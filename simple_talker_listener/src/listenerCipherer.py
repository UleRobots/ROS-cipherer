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
    
def decrypt_chunk(chunk):
    #decoded_encrypted_data = b64decode(chunk)
    decoded_encrypted_data = chunk
    
    method_ = rospy.get_param('~ciphering')
    SECRET_KEY = rospy.get_param('~secret_key')
    IV = decoded_encrypted_data[:AES.block_size]
    
    if method_ == "AES":
        encryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    elif method_ == "3DES":
        encryptor = DES3.new(SECRET_KEY, DES3.MODE_CFB, IV)
    else:
        rospy.logerr('Invalid encryption method: %s', method_)
            
    #decrypted_data = encryptor.decrypt(decoded_encrypted_data)
    decrypted_data = encryptor.decrypt(decoded_encrypted_data[AES.block_size:])
    decrypted_stripped = StripPadding(decrypted_data, INTERRUPT, PAD)
    
    tag_received = decrypted_stripped[:10]
    tag = "%s" % rospy.get_rostime().nsecs
    
    rospy.loginfo(rospy.get_caller_id() + ' - tag: %s, tag_received: %s', tag, tag_received)
    
    if tag != tag_received:
        return
    
    msg = decrypted_stripped[10:]
    
    return msg

def StripPadding(data, interrupt, pad):
    return data.rstrip(pad).rstrip(interrupt) 
                
def callback(data):
    msg = decrypt_chunk(data.data)
    
    if msg:
        rospy.loginfo(rospy.get_caller_id() + ' - I heard: %s ', msg)
    
def listener():
    rospy.init_node('listener', anonymous=True)    
    rospy.Subscriber('chatter', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    #This sleep is needed for synchronization
    time.sleep(3)
    listener()

