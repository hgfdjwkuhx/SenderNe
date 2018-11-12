from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
#from .models import Dialog
from django.db.models import Q
import logging
import sys

import threading


# main user
from SenderNeClientAPI.models import UserPrivateProcessorInfo , ProcessorInfo , TempUserPrivateProcessorInfo

main_User_Lock = threading.Lock()


def get_user_from_session(session_key):
    #main_User_Lock.acquire()
    """
    Gets the user from current User model using the passed session_key
    :param session_key: django.contrib.sessions.models.Session - session_key
    :return: User instance or None if not found
    """
    session = None
    try:
        session = Session.objects.get(session_key=session_key)
    except:
        return None
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')
    user = get_user_model().objects.filter(id=uid).first()  # get object or none

    #main_User_Lock.release()

    return user

# user processor info Model
main_UserProcessorInfo_Lock = threading.Lock()

def get_userProcessorInfo_from_session(session_key):

    #main_UserProcessorInfo_Lock.acquire()
    userProcessorInfo_Model = None
    user_model = get_user_from_session(session_key)
    if user_model is not None:
        userProcessorInfo_Model = UserPrivateProcessorInfo.objects.get(owner=user_model)
        if userProcessorInfo_Model is None:
            raise Exception("user is not exist")
        return userProcessorInfo_Model
    else:
        #raise Exception("user model is not exist")
        return None

    #main_UserProcessorInfo_Lock.release()

    # user processor info Model


main_ProcessorInfo_Lock = threading.Lock()

def get_processorInfo_from_session(session_key):
    # main_ProcessorInfo_Lock.acquire()
    processor_model = ProcessorInfo.objects.get(processor_token=session_key)
    if processor_model is not None:
        return processor_model
    else:
        raise Exception("processor model is not exist")
        #return None
    # main_ProcessorInfo_Lock.release()

main_TempUserProcessorInfo_Lock = threading.Lock()
def get_tempUserProcessorInfo_from_session(session_key):
    # main_TempUserProcessorInfo_Lock.acquire()
    tempUser_model = TempUserPrivateProcessorInfo.objects.get(temp_token=session_key)
    if tempUser_model is not None:
        return tempUser_model
    else:
        raise Exception("tempUser model is not exist")
        #return None
    # main_TempUserProcessorInfo_Lock.release()



def get_dialogs_with_user(user_1, user_2):
    """
    gets the dialog between user_1 and user_2
    :param user_1: the first user in dialog (owner or opponent)
    :param user_2: the second user in dialog (owner or opponent)
    :return: queryset which include dialog between user_1 and user_2 (queryset can be empty)
    """
    #return Dialog.objects.filter(Q(owner=user_1, opponent=user_2) | Q(opponent=user_1, owner=user_2))


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt='%d.%m.%y %H:%M:%S')
logger = logging.getLogger('django-private-dialog')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
