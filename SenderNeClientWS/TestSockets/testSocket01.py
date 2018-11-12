import asyncio
#import tornado.web

#import asyncio
import ssl
import time

import websockets
from django.conf import settings
#from django.core.management.base import BaseCommand
from SenderNeClientWS import channels, handlers
from SenderNeClientWS.utils import logger

class WebServer(object):

    def __init__(self):
        pass

    def run(self, port=8886):
        #self.listen(port)
        #tornado.ioloop.IOLoop.instance().start()
        help = 'Starts message center chat engine'

        #def handle(self, *args, **options):
        #if options['ssl_cert'] is not None:
        #    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
         #   ssl_context.load_cert_chain(options['ssl_cert'])
        #else:
         #   ssl_context = None
        ssl_context = None

        asyncio.async(
            websockets.serve(
                handlers.main_handler,
                settings.CHAT_WS_SERVER_HOST,
                settings.CHAT_WS_SERVER_PORT,
                ssl=ssl_context
            )
        )

        logger.info('Chat server started')
        # asyncio.async(handlers.new_messages_handler(channels.new_messages))
        asyncio.async(handlers.users_changed_handler(channels.users_changed))
        # asyncio.async(handlers.gone_online(channels.online))
        # asyncio.async(handlers.check_online(channels.check_online))
        # asyncio.async(handlers.gone_offline(channels.offline))
        # asyncio.async(handlers.is_typing_handler(channels.is_typing))
        # asyncio.async(handlers.read_message_handler(channels.read_unread))

        # asyncio.async(handlers.send_client_handler(channels.send_client))
        asyncio.async(handlers.new_client_processor_request_handler(channels.client_processor_requests))
        asyncio.async(handlers.new_processor_request_handler(channels.processor_requests))

        asyncio.async(handlers.processor_ack_request_handler(channels.processor_request_acks))

        # loop = asyncio.get_event_loop()
        loop = asyncio.get_event_loop()
        loop.run_forever()









ws = WebServer()


def start_server():
    time.sleep(3)
    #asyncio.set_event_loop(asyncio.new_event_loop())
    ws.run()


from threading import Thread
t = Thread(target=start_server, args=())
t.daemon = True
t.start()

t.join()