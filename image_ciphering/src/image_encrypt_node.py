#!/usr/bin/env python

"""
NOTA: Part of the code is using OpenCV features with ros CompressedImage Topics in python,
by Simon Haller <simon.haller at uibk.ac.at>.
"""


# Python libs
import sys, time, datetime

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

from Crypto.Cipher import DES3
from Crypto.Cipher import AES

from Crypto import Random
from base64 import b64encode, b64decode

from struct import pack


MODE_AES = 0
MODE_3DES = 1

# AES is a block cipher so you need to define size of block.
# Valid options are 16, 24, and 32
BLOCK_SIZE = 16 
INTERRUPT = u'\u0001'
PAD = u'\u0000'

INPUT_SIZE = 8

VERBOSE=True


class fps:
        def __init__(self):
                # store the start time, end time, and total number of frames
                # that were examined between the start and end intervals
                self._start = None
                self._end = None
                self._numFrames = 0

        def start(self):
                # start the timer
                self._start = datetime.datetime.now()
                return self

        def stop(self):
                # stop the timer
                self._end = datetime.datetime.now()

        def update(self):
                # increment the total number of frames examined during the
                # start and end intervals
                self._numFrames += 1

        def elapsed(self):
                # return the total number of seconds between the start and
                # end interval
                return (self._end - self._start).total_seconds()

        def fps(self):
                # compute the (approximate) frames per second
                return self._numFrames / self.elapsed()
        
        def partialfps(self):
                # compute the (approximate) frames per second
                return self._numFrames / (datetime.datetime.now() - self._start).total_seconds()


class image_encrypt:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        self.image_pub = rospy.Publisher("/output/image_encrypted/compressed",
            CompressedImage, queue_size = 1)
        # self.bridge = CvBridge()
      
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/camera/rgb/image_raw/compressed",
            CompressedImage, self.callback,  queue_size = 1)
        if VERBOSE:
            print "subscribed to /camera/image/compressed"
        
        self.enc_mode = -1
         # parameters for lm and dic
        try:
            method_ = rospy.get_param('~ciphering')
	    #rospy.logwarn('Encryption method: %s', method_)
	    
	    self.enc_mode = self.set_mode(method_)
    	    
            if (self.enc_mode == MODE_3DES):
              self.key_3DES = '0123456701234567'
              self.iv_3DES = ';;;;;;;;'
              
            elif (self.enc_mode == MODE_AES):               
              SECRET_KEY = u'a1b2c3d4e5f6g7h8a1b2c3d4e5f6g7h8'
              IV = u'12345678abcdefgh'
              self.key_AES = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
              
	    elif (self.enc_mode == -1):
	      return
	    
        except:
            rospy.logerr('Please specify an encryption method!')
            return

        self.fps = fps().start()
    
    
    # Since you need to pad your data before encryption, 
    # create a padding function as well
    # Similarly, create a function to strip off the padding after decryption
    def AddPadding(self, data, interrupt, pad, block_size):
	new_data = ''.join([data, interrupt])
	new_data_len = len(new_data)
	remaining_len = block_size - new_data_len
	to_pad_len = remaining_len % block_size
	pad_string = pad * to_pad_len
	return ''.join([new_data, pad_string])
      
    
    def encrypt_chunk_3DES(self, chunk,key, iv):
        des3 = DES3.new(key, DES3.MODE_CFB, iv)
        if len(chunk) == 0:
          print "empty chain"
        elif len(chunk) % 16 != 0:
          chunk += ' ' * (16 - len(chunk) % 16)
        chunk = des3.encrypt(chunk)
        return chunk
  
    def encrypt_chunk_AES(self, chunk):
	if len(chunk) % 16 != 0:
	  chunk += ' ' * (16 - len(chunk) % 16)
	ciphertext = self.key_AES.encrypt(chunk)
	return ciphertext
  
    def set_mode(self, mode):
	encryption_mode = -1
	rospy.logwarn('Encryption method: %s', mode)
	if(mode in "AES"):
	  encryption_mode = MODE_AES
	elif(mode in "3DES"):
	  encryption_mode = MODE_3DES
	return encryption_mode
	
    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and encrypted'''
        
        # print 'DEBUG: received image of type: "%s"' % ros_data.format

        #### direct conversion to CV2 ####
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        image_np_with_text = cv2.copyMakeBorder(image_np,0,0,0,0,cv2.BORDER_REPLICATE) 
        
        #cv2.putText(image_np_with_text,"{:.2f}".format(self.fps.partialfps()),(10,470), font, 1,(255,255,255),2)
        #cv2.imshow('Before_Encryption', image_np_with_text)
        #cv2.waitKey(2)
        #self.fps.update()
                
        #### Create CompressedIamge ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()

        if ( self.enc_mode == MODE_3DES):
	  msg.data = self.encrypt_chunk_3DES(msg.data, self.key_3DES, self.iv_3DES)

	elif (self.enc_mode == MODE_AES):
          msg.data =  b64encode(msg.data)
	  plaintext_padded = self.AddPadding(msg.data, INTERRUPT, PAD, BLOCK_SIZE)
	  encrypted = self.encrypt_chunk_AES(plaintext_padded)
	  msg.data =  b64encode(encrypted)

        # Publish new image
        self.image_pub.publish(msg)
        
    def exit(self):
        # stop the timer and display FPS information
        self.fps.stop()
        print("[INFO] Encrypter node:  elasped time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] Encrypter node:  approx. FPS: {:.2f}".format(self.fps.fps()))

    
def main(args):
    '''Initializes and cleans up ros node'''
   
    rospy.init_node('image_encrypt', anonymous=True)
    img_enc = image_encrypt()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS image encrypter."
    img_enc.exit()
    #cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
