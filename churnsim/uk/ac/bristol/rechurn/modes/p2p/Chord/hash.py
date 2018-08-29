import hashlib

def chord_hash(keystring):
    hashedobj = hash(keystring)%256
    return hashedobj

def sha6hash(keystring):
    hashedobj = hashlib.sha1(keystring.encode('utf-8'))
    return hashedobj.hexdigest()
