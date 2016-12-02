#!/usr/bin/env python

## First approach: ciphering the talker messages with AES.

# The talker node  that published std_msgs/Strings messages
# to the 'chatter' topic.

import rospy
from std_msgs.msg import String
import os
from Crypto.Cipher import AES
from Crypto import Random

from base64 import b64encode, b64decode
from re import sub
from datetime import datetime

# AES is a block cipher so you need to define size of block.
# Valid options are 16, 24, and 32
BLOCK_SIZE = 16 
INTERRUPT = u'\u0001'
PAD = u'\u0000'

# Since it is needed to pad your data before encryption, 
# we create a padding function as well.
def AddPadding(data, interrupt, pad, block_size):
    new_data = ''.join([data, interrupt])
    new_data_len = len(new_data)
    remaining_len = block_size - new_data_len
    to_pad_len = remaining_len % block_size
    pad_string = pad * to_pad_len
    return ''.join([new_data, pad_string])

# Similarly, create a function to strip off the padding after decryption.  
def StripPadding(data, interrupt, pad):
    return data.rstrip(pad).rstrip(interrupt)

def encrypt_chunk_AES(chunk,encryptor):
    #if len(chunk) == 0:
      #break
    if len(chunk) % 16 != 0:
      chunk += ' ' * (16 - len(chunk) % 16)
    ciphertext = encryptor.encrypt(chunk)
    return ciphertext

def talker():    
    SECRET_KEY = u'a1b2c3d4e5f6g7h8a1b2c3d4e5f6g7h8'
    IV = u'12345678abcdefgh'

    encryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
    
    decryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

    #plaintext_data = 'Secret Message A'
    #plaintext_padded = AddPadding(plaintext_data, INTERRUPT, PAD, BLOCK_SIZE)
    #encrypted = encryptor.encrypt(plaintext_padded)
    #decrypted =  b64encode(encrypted)
    #print decrypted 
    
    #decoded_encrypted_data = b64decode(decrypted)
    #decrypted_data = decryptor.decrypt(decoded_encrypted_data)
    #print StripPadding(decrypted_data, INTERRUPT, PAD)
    #print "==============================="
    
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        #print "********1"
        #print hello_str
         
        #if len(hello_str) % 16 != 0:
          #hello_str += ' ' * (16 - len(hello_str) % 16)
        #print hello_str
        #cadenilla = encryptor.encrypt(hello_str)
        
        #print cadenilla
        #print decryptor.decrypt(cadenilla)
        #pub.publish( "".join(encrypt_chunk_AES(hello_str, encryptor)))
        #print decryptor.decrypt("".join(encrypt_chunk_AES(hello_str, encryptor)))
        #print "********2"
        plaintext_padded = AddPadding(hello_str, INTERRUPT, PAD, BLOCK_SIZE)
        encrypted = encryptor.encrypt(plaintext_padded)
        pub.publish(b64encode(encrypted))

        #print decryptor.decrypt("".join(encrypt_chunk_AES(hello_str, encryptor)))
        #pub.publish(encrypt_chunk_AES(hello_str, key))
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

