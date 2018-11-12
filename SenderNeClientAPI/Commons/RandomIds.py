import random
import string
import operator






def get_random_ObjectId():
    return (''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])).lower()



def get_random_PrivateUserStore_dbName():
    return (''.join([random.choice(string.ascii_letters ) for n in range(32)])).lower()


def get_random_PrivateUserStore_storeName():
    return (''.join([random.choice(string.ascii_letters ) for n in range(30)])).lower()


def get_random_PrivateUser_userObjectId():
    return (''.join([random.choice(string.ascii_letters ) for n in range(42)])).lower()

def get_random_PrivateUser_TempUserObjectId():
    return (''.join([random.choice(string.ascii_letters ) for n in range(65)])).lower()

def get_random_PrivateProcessor_processorObjectId():
    return (''.join([random.choice(string.ascii_letters ) for n in range(60)])).lower()

def get_random_PrivateProcessor_processorToken():
    return (''.join([random.choice(string.ascii_letters ) for n in range(50)]))


def get_random_PrivateTempUser_TempUserToken():
    return (''.join([random.choice(string.ascii_letters ) for n in range(68)]))







