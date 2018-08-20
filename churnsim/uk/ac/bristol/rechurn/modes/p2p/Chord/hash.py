import hashlib

def chord_hash(self, keystring):
    hashedobj = hashlib.sha1(keystring)
    return hashedobj.hexdigest()
