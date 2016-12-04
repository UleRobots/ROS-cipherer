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

# Metodo en el que se descifra el mensaje recibido en funcion del metodo seleccionado
def decrypt_chunk(chunk):
    decoded_encrypted_data = chunk
    
    method_ = rospy.get_param('~ciphering') # get ciphering param: AES (default) or 3DES
    SECRET_KEY = rospy.get_param('~secret_key') # get secret key
    IV = decoded_encrypted_data[:AES.block_size] # get IV from received message
    
    if method_ == "AES":
        encryptor = AES.new(SECRET_KEY, AES.MODE_CBC, IV) # init AES cipher
    elif method_ == "3DES":
        encryptor = DES3.new(SECRET_KEY, DES3.MODE_CFB, IV) # init 3DES cipher
    else:
        rospy.logerr('Invalid encryption method: %s', method_)
    
    decrypted_data = encryptor.decrypt(decoded_encrypted_data[AES.block_size:]) # Decrypt message (without IV)
    decrypted_stripped = StripPadding(decrypted_data, INTERRUPT, PAD)
    
    tag_received = decrypted_stripped[:10] # get tag from received message
    tag = "%s" % rospy.get_rostime().secs # calculate local tag
    
    # DEBUG:
    # rospy.loginfo(rospy.get_caller_id() + ' - tag: %s, tag_received: %s', tag, tag_received)
    
    if tag != tag_received: # if received tag is not equal to local tag we have finished
        return
    
    msg = decrypted_stripped[10:] # get message
    
    return msg

def StripPadding(data, interrupt, pad):
    return data.rstrip(pad).rstrip(interrupt) 

# Metodo que muestra por pantalla el mensaje recibido descrifrado                
def callback(data):
    msg = decrypt_chunk(data.data)
    
    if msg:
        rospy.loginfo(rospy.get_caller_id() + ' - I heard: %s ', msg)

# Metodo en el que se crea un nodo y se suscribe al topic chatter
def listener():
    rospy.init_node('listener', anonymous=True)     # init node
    rospy.Subscriber('chatter', String, callback)   # suscribe chatter topic

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    #This sleep is needed for synchronization
    time.sleep(1)
    listener()

