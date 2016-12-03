#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import os
from Crypto import Random
from Crypto.Cipher import AES, DES3
import time
from functools import wraps
 
from base64 import b64encode, b64decode
from re import sub
from datetime import datetime

# AES listener.

# AES is a block cipher so you need to define size of block.
# Valid options are 16, 24, and 32
BLOCK_SIZE = 16
INTERRUPT = u'\u0001'
PAD = u'\u0000'

def decrypt_chunk_DES3(chunk):
    if len(chunk) == 0:
      print "empty chain"
    return encryptor.decrypt(chunk)
    
def decrypt_chunk_AES(chunk):
    decoded_encrypted_data = b64decode(chunk)
    decrypted_data = encryptor.decrypt(decoded_encrypted_data)
    decrypted_stripped = StripPadding(decrypted_data, INTERRUPT, PAD)
    return decrypted_stripped

def StripPadding(data, interrupt, pad):
    return data.rstrip(pad).rstrip(interrupt) 
                
def callback(data):
    #if method_ == "3DES":
        #rospy.loginfo(rospy.get_caller_id() + 'I heard %s', decrypt_chunk_DES3(data.data))
    #else:
    rospy.loginfo(rospy.get_caller_id() + ' - I heard: %s ', decrypt_chunk_AES(data.data))
def listener():
    global encryptor
    global method_
    
    rospy.init_node('listener', anonymous=True)
    
    try:
        global method_
        method_ = rospy.get_param('~ciphering')
        SECRET_KEY = rospy.get_param('~secret_key')
        IV = rospy.get_param('~IV')
        
        if method_ == "AES":
	    encryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
        #elif method_ == "3DES":
            #encryptor = DES3.new(SECRET_KEY, DES3.MODE_CFB, IV)
        else:
            rospy.logerr('Invalid encryption method: %s', method_)
    except:
        rospy.logerr('Please specify an encryption method!')
        return
    
    rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    #This sleep is needed for synchronization
    time.sleep(3)
    listener()

