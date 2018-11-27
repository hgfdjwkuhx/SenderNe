import asyncio
import json
import logging
import websockets
from django.contrib.auth import get_user_model

from SenderNeClientAPI.Commons.BlockStates import BlockedStatu
from SenderNeClientWS.management.StoreModel.StorePeeWee.ReceiverPrivateStoreManager.PrivateStoreModel import \
    ReceiverRequestsPrivateStoreModel
from . import models, router


from .utils import get_user_from_session,get_userProcessorInfo_from_session, get_dialogs_with_user ,get_processorInfo_from_session ,get_tempUserProcessorInfo_from_session

logger = logging.getLogger('handlers-private-dialog')

ws_connections = {}
users_ws_connections = {}
processors_ws_connections = {}

tempUsers_ws_connections = {}


mainUtilities_users = {}

storeModel = ReceiverRequestsPrivateStoreModel()


@asyncio.coroutine
def target_message(conn, payload):
    """
    Distibuted payload (message) to one connection
    :param conn: connection
    :param payload: payload(json dumpable)
    :return:
    """
    try:
        yield from conn.send(json.dumps(payload))
    except Exception as e:
        logger.debug('could not send', e)


@asyncio.coroutine
def fanout_message(connections, payload):
    """
    Distributes payload (message) to all connected ws clients
    """
    for conn in connections:
        try:
            yield from conn.send(json.dumps(payload))
        except Exception as e:
            logger.debug('could not send', e)


@asyncio.coroutine
def gone_online(stream):
    """
    Distributes the users online status to everyone he has dialog with
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        if session_id:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                logger.debug('User ' + user_owner.username + ' gone online')
                # find all connections including user_owner as opponent,
                # send them a message that the user has gone online
                online_opponents = list(filter(lambda x: x[1] == user_owner.username, ws_connections))
                online_opponents_sockets = [ws_connections[i] for i in online_opponents]
                yield from fanout_message(online_opponents_sockets,
                                          {'type': 'gone-online', 'usernames': [user_owner.username]})
            else:
                pass  # invalid session id
        else:
            pass  # no session id


@asyncio.coroutine
def check_online(stream):
    """
    Used to check user's online opponents and show their online/offline status on page on init
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        opponent_username = packet.get('username')
        if session_id and opponent_username:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                # Find all connections including user_owner as opponent
                online_opponents = list(filter(lambda x: x[1] == user_owner.username, ws_connections))
                logger.debug('User ' + user_owner.username + ' has ' + str(len(online_opponents)) + ' opponents online')
                # Send user online statuses of his opponents
                socket = ws_connections.get((user_owner.username, opponent_username))
                if socket:
                    online_opponents_usernames = [i[0] for i in online_opponents]
                    yield from target_message(socket,
                                              {'type': 'gone-online', 'usernames': online_opponents_usernames})
                else:
                    pass  # socket for the pair user_owner.username, opponent_username not found
                    # this can be in case the user has already gone offline
            else:
                pass  # invalid session id
        else:
            pass  # no session id or opponent username


@asyncio.coroutine
def gone_offline(stream):
    """
    Distributes the users online status to everyone he has dialog with
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        if session_id:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                logger.debug('User ' + user_owner.username + ' gone offline')
                # find all connections including user_owner as opponent,
                #  send them a message that the user has gone offline
                online_opponents = list(filter(lambda x: x[1] == user_owner.username, ws_connections))
                online_opponents_sockets = [ws_connections[i] for i in online_opponents]
                yield from fanout_message(online_opponents_sockets,
                                          {'type': 'gone-offline', 'username': user_owner.username})
            else:
                pass  # invalid session id
        else:
            pass  # no session id


@asyncio.coroutine
def new_messages_handler(stream):
    """
    Saves a new chat message to db and distributes msg to connected users
    """
    # TODO: handle no user found exception
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        msg = packet.get('message')
        username_opponent = packet.get('username')
        if session_id and msg and username_opponent:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                user_opponent = get_user_model().objects.get(username=username_opponent)
                dialog = get_dialogs_with_user(user_owner, user_opponent)
                if len(dialog) > 0:
                    # Save the message
                    msg = models.Message.objects.create(
                        dialog=dialog[0],
                        sender=user_owner,
                        text=packet['message'],
                        read=False
                    )
                    packet['created'] = msg.get_formatted_create_datetime()
                    packet['sender_name'] = msg.sender.username
                    packet['message_id'] = msg.id

                    # Send the message
                    connections = []
                    # Find socket of the user which sent the message
                    if (user_owner.username, user_opponent.username) in ws_connections:
                        connections.append(ws_connections[(user_owner.username, user_opponent.username)])
                    # Find socket of the opponent
                    if (user_opponent.username, user_owner.username) in ws_connections:
                        connections.append(ws_connections[(user_opponent.username, user_owner.username)])
                    else:
                        # Find sockets of people who the opponent is talking with
                        opponent_connections = list(filter(lambda x: x[0] == user_opponent.username, ws_connections))
                        opponent_connections_sockets = [ws_connections[i] for i in opponent_connections]
                        connections.extend(opponent_connections_sockets)

                    yield from fanout_message(connections, packet)
                else:
                    pass  # no dialog found
            else:
                pass  # no user_owner
        else:
            pass  # missing one of params


@asyncio.coroutine
def users_changed_handler(stream):
    """
    Sends connected client list of currently active users in the chatroom
    """
    while True:
        yield from stream.get()

        # Get list list of current active users
        users = [
            {'username': username, 'uuid': uuid_str}
            for username, uuid_str in ws_connections.values()
        ]

        # Make packet with list of new users (sorted by username)
        packet = {
            'type': 'users-changed',
            'value': sorted(users, key=lambda i: i['username'])
        }
        logger.debug(packet)
        yield from fanout_message(ws_connections.keys(), packet)


@asyncio.coroutine
def is_typing_handler(stream):
    """
    Show message to opponent if user is typing message
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        user_opponent = packet.get('username')
        typing = packet.get('typing')
        if session_id and user_opponent and typing is not None:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                opponent_socket = ws_connections.get((user_opponent, user_owner.username))
                if typing and opponent_socket:
                    yield from target_message(opponent_socket,
                                              {'type': 'opponent-typing', 'username': user_opponent})
            else:
                pass  # invalid session id
        else:
            pass  # no session id or user_opponent or typing


@asyncio.coroutine
def read_message_handler(stream):
    """
    Send message to user if the opponent has read the message
    """
    while True:
        packet = yield from stream.get()
        session_id = packet.get('session_key')
        user_opponent = packet.get('username')
        message_id = packet.get('message_id')
        if session_id and user_opponent and message_id is not None:
            user_owner = get_user_from_session(session_id)
            if user_owner:
                message = models.Message.filter(id=message_id).first()
                if message:
                    message.read = True
                    message.save()
                    logger.debug('Message ' + str(message_id) + ' is now read')
                    opponent_socket = ws_connections.get((user_opponent, user_owner.username))
                    if opponent_socket:
                        yield from target_message(opponent_socket,
                                                  {'type': 'opponent-read-message',
                                                   'username': user_opponent, 'message_id': message_id})
                else:
                    pass  # message not found
            else:
                pass  # invalid session id
        else:
            pass  # no session id or user_opponent or typing



@asyncio.coroutine
def main_handler(websocket, path):
    """
    An Asyncio Task is created for every new websocket client connection
    that is established. This coroutine listens to messages from the connected
    client and routes the message to the proper queue.

    This coroutine can be thought of as a producer.
    """
    # Get users name from the path

    #print("\npath == " + path)
    #print("\nwebsocket : type == " + str(type(websocket)))

    path = path.split('/')
    #username = path[2]
    session_id = path[1]

    #-------- For Get User Or Process ------------#
    # AA check User Socket
    user_processor_info = get_userProcessorInfo_from_session(session_id)
    if user_processor_info is not None:
        print("\n################# is User ######################")

        user_objectId = user_processor_info.user_objectId
        # 01 check UserObject Id
        #
        #
        #

        # 02 Check Blocked State
        blocked_statu = user_processor_info.blocked_state
        #
        #
        #
        #
        if not blocked_statu == BlockedStatu.Running:
            #send to user blocked state
            raise Exception("user is blocked")
        else:
            # 03 Check processor
            if user_processor_info.processor_info is None:
                raise Exception("user have not processor info")

            # 04 Check processor ws
            processor_ws = processors_ws_connections.get(user_processor_info.processor_info.processor_ObjectId)
            if processor_ws is not None:
                users_ws_connections[user_objectId] = {
                    "processor_objectId" : processor_ws["processor_objectId"],
                    "websocket" : websocket ,
                    "user_objectId" : user_objectId
                }
                try:
                    while websocket.open:
                        data = yield from websocket.recv()
                        if not data:
                            print("\n----- : websocket.recv() : not data : -----------")
                            continue
                        logger.debug(data)
                        print("client : data == " + str(data))
                        # as temp truing
                        # main_tag_handler(data)

                        try:
                            yield from router.UserRequestRouter(data , user_objectId)()
                        except Exception as e:
                            logger.error('could not route msg', e)

                except websockets.exceptions.InvalidState:  # User disconnected
                    pass
                finally:
                    # del ws_connections[(user_owner, username)]
                    # del mainUtilities_users[user_owner_model]
                    del users_ws_connections[user_objectId]
            else:
                #save request in requests DB
                raise Exception("processor_ws is not connect")

    else:
        # BB check Processor Socket
        if session_id.__len__() == 50:
            print("\n################# is Processor ######################")
            processor_model = get_processorInfo_from_session(session_id)
            if processor_model is not None:
                processor_objectId = processor_model.processor_ObjectId
                # 01 check processor_ObjectId
                #
                #
                #

                # 02 Check Blocked State
                #blocked_statu = user_processor_info.blocked_state
                #
                #
                #
                #

                # 03 check exsist
                if processors_ws_connections.get(processor_objectId) is not None:
                    del processors_ws_connections[processor_objectId]

                # 04
                processors_ws_connections[processor_objectId] = {
                    "websocket" : websocket,
                    "processor_objectId" : processor_objectId
                }
                try:
                    while websocket.open:
                        data = yield from websocket.recv()
                        if not data:
                            print("\n----- : processor_websocket.recv() : not data : -----------")
                            continue
                        logger.debug(data)
                        print("processo : data == " + str(data))

                        # as temp truing
                        # main_tag_handler(data)

                        try:
                            yield from router.ProcessorRequestRouter(data , processor_objectId)()
                        except Exception as e:
                            logger.error('could not route msg', e)

                except websockets.exceptions.InvalidState:  # User disconnected
                    pass
                finally:
                    del processors_ws_connections[processor_objectId]
            else:
                raise Exception("processor model is not exist")

        else:
            # CC check TempUser Socket
            if session_id.__len__() == 86:
                tempUser_model = get_tempUserProcessorInfo_from_session(session_id)
                if tempUser_model is not None:
                    tempUser_objectId = tempUser_model.user_objectId
                    # 01 check user_objectId
                    #
                    #
                    #

                    # 02 Check Blocked State
                    blocked_statu = tempUser_model.blocked_state
                    #
                    #
                    #
                    #
                    # 04 check blocked_statu
                    if not blocked_statu == BlockedStatu.Running:
                        # save in temp db
                        raise Exception("Temp user is Blocked")
                    else:

                        # 05 Check processor
                        if tempUser_model.processor_info is None:
                            raise Exception("user have not processor info")

                        else:
                            # 06 Check processor ws
                            processor_ws = processors_ws_connections.get(
                                tempUser_model.processor_info.processor_ObjectId)
                            if processor_ws is not None:
                                # 07 check exsist
                                if tempUsers_ws_connections.get(tempUser_objectId) is not None:
                                    del tempUsers_ws_connections[tempUser_objectId]

                                tempUsers_ws_connections[tempUser_objectId] = {
                                "websocket": websocket,
                                "tempUser_objectId": tempUser_objectId,
                                "processor_ws" : processor_ws
                                }
                                try:
                                    while websocket.open:
                                        data = yield from websocket.recv()
                                        if not data:
                                            print("\n----- : tempUser_websocket.recv() : not data : -----------")
                                            continue
                                        logger.debug(data)

                                        # as temp truing
                                        # main_tag_handler(data)

                                        try:
                                            # yield from router.MessageRouter(data)()
                                            pass
                                        except Exception as e:
                                            logger.error('could not route msg', e)

                                except websockets.exceptions.InvalidState:  # User disconnected
                                    pass
                                finally:
                                    del tempUsers_ws_connections[tempUser_objectId]

                            else:
                                raise Exception("processor ws is not running")
                else:
                    raise Exception("tempUser model is not exist")

            else:
                logger.info("Got invalid session_id attempt to connect " + session_id)

@asyncio.coroutine
def target_message_processor(processor_ws, payload , isJson = False):
    """
    Distibuted payload (message) to one connection
    :param conn: connection
    :param payload: payload(json dumpable)
    :return:
    """
    if isJson:
        try:
            yield from processor_ws.send(payload)
        except Exception as e:
            logger.debug('could not send', e)
    else:
        try:
            yield from processor_ws.send(json.dumps(payload))
        except Exception as e:
            logger.debug('could not send', e)

@asyncio.coroutine
def new_client_processor_request_handler(stream):
    """
    router a request to processor socket
    """
    # TODO: handle no user found exception
    while True:
        user_objectId , packet = yield from stream.get()

        req_model = storeModel.UserProcessorHandleRequest(
            user_objectId=user_objectId
        )
        packet["user_objectId"] = user_objectId
        packet["req-type"] = "client"
        req_model.request_id = packet.get("id")
        req_model.row_data = json.dumps(packet)

        user_connection = users_ws_connections.get(user_objectId)
        if user_connection is not None:

            processor_ws = processors_ws_connections.get(user_connection.get("processor_objectId"))
            if processor_ws is not None:

                req_model.processor_objectId = processor_ws["processor_objectId"]

                yield from target_message_processor(processor_ws["websocket"], req_model.row_data , True)
            else:
                raise Exception("processor_ws is None")
        else:
            raise Exception("user connection is not exist")

        #req_model.save_toQueue()
        req_model.save()

@asyncio.coroutine
def target_message_user(user_ws, payload):
    """
    Distibuted payload (message) to one connection
    :param conn: connection
    :param payload: payload(json dumpable)
    :return:
    """
    try:
        yield from user_ws.send(json.dumps(payload))
    except Exception as e:
        logger.debug('could not send', e)



@asyncio.coroutine
def new_processor_request_handler(stream):
    """
    router a request to user socket
    """
    # TODO: handle no user found exception
    while True:
        processor_objectId , packet = yield from stream.get()

        #data = json.loads(packet)
        data = packet
        if data is not None:

            user_id = data.get("user_id")
            if user_id is not None:
                if type(user_id) is str:
                    ## check here later if user is registed or tempUser
                    # that by userId length
                    user_connection = users_ws_connections.get(user_id)
                    if user_connection is not None:
                        payload = data.get("data")
                        if payload is not None:
                            if type(payload) is dict:
                                yield from target_message_user(user_connection["websocket"], payload)
                            else:
                                raise Exception("error in payload : type")
                        else:
                            raise Exception("error in payload : null")
                    else:
                        # save the result in temp db users result
                        raise Exception("may user ws is close")
                else:
                    raise Exception("error in user_id : type")
            else:
                raise Exception("here may sys notifi")
        else:
            raise Exception("error in packet : null")

@asyncio.coroutine
def processor_ack_request_handler(stream):
    """
    router a request to user socket
    """
    # TODO: handle no user found exception
    while True:
        processor_objectId , packet = yield from stream.get()

        #data = json.loads(packet)
        data = packet
        if data is not None:
            node_id = data.get("node_id")
            if node_id is not None:
                if type(node_id) is str:
                    request_type = data.get("request_type")
                    if type(request_type) is str:
                        if request_type == "client":
                            req_model = storeModel.UserProcessorHandleRequest.get_or_none(
                                (storeModel.UserProcessorHandleRequest.user_objectId == data.get("user_id")) &
                                (storeModel.UserProcessorHandleRequest.request_id == node_id)
                            )
                            if req_model is not None:
                                req_model.request_state = storeModel.HandleRequestState.processorAck
                                req_model.save()
                            else:
                                raise Exception("req_model is not exist")
                        else:
                            raise Exception("here may request_type == sys")
                    else:
                        raise Exception("error in request_type : type")
                else:
                    raise Exception("error in node_id : type")
            else:
                raise Exception("error in node_id : null")
        else:
            raise Exception("error in packet : null")

