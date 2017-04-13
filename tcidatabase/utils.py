import hashlib
import random


def generate_key(string=''):
    if not string:
        string = str(random())
    sha = hashlib.md5(string.encode('utf-8'))
    return sha.hexdigest()
