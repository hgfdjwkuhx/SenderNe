import asyncio
try:
    import Queue
except ImportError:
    import queue as Queue



new_messages = asyncio.Queue()
users_changed = asyncio.Queue()
online = asyncio.Queue()
offline = asyncio.Queue()
check_online = asyncio.Queue()
is_typing = asyncio.Queue()
read_unread = asyncio.Queue()


send_client = asyncio.Queue()



client_processor_requests = asyncio.Queue()
processor_requests = asyncio.Queue()

processor_request_acks = asyncio.Queue()







def put_user_notify(conn , payload):
    #print("\n--------------- : put_user_notify ; ----------------------")
    send_client.put_nowait((conn , payload))




#-------------- For Processors --------------------#

#process_request = asyncio.Queue()