#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import os
from Crypto import Random
from Crypto.Cipher import AES
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
             
def decrypt_chunk_AES(chunk):
    encrypted = chunk
    decoded_encrypted_data = b64decode(encrypted)
    decrypted_data = cipher_for_decryption.decrypt(decoded_encrypted_data)
    decrypted = StripPadding(decrypted_data, INTERRUPT, PAD)
    return decrypted

def StripPadding(data, interrupt, pad):
    return data.rstrip(pad).rstrip(interrupt)  
                
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + ' - I heard: %s ', decrypt_chunk_AES(data.data))

def listener():
    SECRET_KEY = u'a1b2c3d4e5f6g7h8a1b2c3d4e5f6g7h8'
    IV = u'12345678abcdefgh'

    global cipher_for_decryption
    cipher_for_decryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    #This sleep is needed for synchronization
    time.sleep(3)
    listener()

