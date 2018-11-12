import asyncio
import json
import logging

from .channels import new_messages, users_changed, online, offline, check_online, is_typing, read_unread , send_client , client_processor_requests , processor_requests , processor_request_acks

logger = logging.getLogger('django-SenderNe-ClientWS')


class MessageRouter(object):
    MESSAGE_QUEUES = {
        'new-message': new_messages,
        'new-user': users_changed,
        'online': online,
        'offline': offline,
        'check-online': check_online,
        'is-typing': is_typing,
        'read_message': read_unread
        #'send_client' : send_client
    }

    def __init__(self, data):
        try:
            self.packet = json.loads(data)
        except Exception as e:
            logger.debug('could not load json: {}'.format(str(e)))

    def get_packet_type(self):
        return self.packet['type']

    @asyncio.coroutine
    def __call__(self):
        logger.debug('routing message: {}'.format(self.packet))
        send_queue = self.get_send_queue()
        yield from send_queue.put(self.packet)

    def get_send_queue(self):
        return self.MESSAGE_QUEUES[self.get_packet_type()]


class UserRequestRouter(object):
    MESSAGE_QUEUES = {
        'campaign' : client_processor_requests
    }

    def __init__(self, data , user_objectId):
        try:
            self.user_objectId = user_objectId
            self.packet = json.loads(data)
        except Exception as e:
            logger.debug('could not load json: {}'.format(str(e)))

    def get_packet_type(self):
        return self.packet['data'].get('tag')

    @asyncio.coroutine
    def __call__(self):
        logger.debug('routing message: {}'.format(self.packet))
        send_queue = self.get_send_queue()
        yield from send_queue.put((self.user_objectId , self.packet))

    def get_send_queue(self):
        return self.MESSAGE_QUEUES[self.get_packet_type()]



class ProcessorRequestRouter(object):
    MESSAGE_QUEUES = {
        'client-result' : processor_requests,
        'node_ack': processor_request_acks
    }

    def __init__(self, data , processor_objectId):
        try:
            self.processor_objectId = processor_objectId
            self.packet = json.loads(data)
        except Exception as e:
            logger.debug('could not load json: {}'.format(str(e)))

    def get_packet_type(self):
        return self.packet['type']

    @asyncio.coroutine
    def __call__(self):
        logger.debug('routing message: {}'.format(self.packet))
        send_queue = self.get_send_queue()
        yield from send_queue.put((self.processor_objectId , self.packet))

    def get_send_queue(self):
        return self.MESSAGE_QUEUES[self.get_packet_type()]
