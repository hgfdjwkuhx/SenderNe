import random
import string
import operator






def get_random_ObjectId():
    return (''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])).lower()






