#!/usr/bin/env python

## First approach: ciphering the talker messages with AES.

# The talker node  that published std_msgs/Strings messages
# to the 'chatter' topic.

import rospy

from std_msgs.msg import String
import os,sys
from Crypto.Cipher import AES,DES3
from Crypto import Random

from base64 import b64encode, b64decode
from re import sub
from datetime import datetime

# AES is a block cipher so you need to define size of block. Valid options are 16, 24, and 32
BLOCK_SIZE = 16 
INTERRUPT = u'\u0001'
PAD = u'\u0000'

# Since it is needed to pad your data before encryption, we create a padding function as well.
def AddPadding(data, interrupt, pad, block_size):
    new_data = ''.join([data, interrupt])
    new_data_len = len(new_data)
    remaining_len = block_size - new_data_len
    to_pad_len = remaining_len % block_size
    pad_string = pad * to_pad_len
    return ''.join([new_data, pad_string])

def talker():    
    pub = rospy.Publisher('chatter', String, queue_size=1) # node publih on /chatter topic
    rospy.init_node('talker', anonymous=True) # register node
    rate = rospy.Rate(10) # 10hz

    try:
        method_ = rospy.get_param('~ciphering') # get cipehering param: AES (default) or 3DES
        SECRET_KEY = rospy.get_param('~secret_key') # get secret_key
    except:
        rospy.logerr('Please, specify an encryption method and a secret key.')
        return
    
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time() # message
        rospy.loginfo(hello_str)

        IV = Random.new().read(BLOCK_SIZE) # IV radomly generated
        
        if method_ == "AES":
            encryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV) # init AES cipher
        elif method_ == "3DES":
            encryptor = DES3.new(SECRET_KEY, DES3.MODE_CFB, IV) # init 3DES cipher
        else:
            rospy.logerr('Invalid encryption method >: %s', method_)
            continue
        
        tag = "%s" % rospy.get_rostime().secs # marca de tiempo
        plaintext_padded = AddPadding(tag + hello_str, INTERRUPT, PAD, BLOCK_SIZE) # add tag at beginning of message
        encrypted = IV + encryptor.encrypt(plaintext_padded)
        pub.publish(encrypted) # send IV and encrypted msg with tag
        
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

