#!/usr/bin/env python

"""
NOTA: Part of the code is using OpenCV features with ros CompressedImage Topics in python,
by Simon Haller <simon.haller at uibk.ac.at>.
"""


# Python libs
import sys, time

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

from Crypto.Cipher import DES3
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode, b64decode

import datetime
import time

MODE_AES = 0
MODE_3DES = 2

START_MODE=0

# AES is a block cipher so you need to define size of block.
# Valid options are 16, 24, and 32
BLOCK_SIZE = 16 
INTERRUPT = u'\u0001'
PAD = u'\u0000'

VERBOSE=True



class FPS:
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


class image_feature:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/output/image_raw/compressed",
            CompressedImage, self.callback,  queue_size = 1)
        if VERBOSE :
            print "subscribed to /camera/image/compressed"
        self.enc_mode = -1
        
        try:
            method_ = rospy.get_param('~mode')
            rospy.logerr('Encryption method: %s', method_)
            
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
  
        self.fps = FPS().start()
    
    
    def set_mode(self, mode):
        encryption_mode = -1
        rospy.logerr('Encryption method: %s', mode)
        if(mode in "AES"):
          encryption_mode = MODE_AES
        elif(mode in "3DES"):
          encryption_mode = MODE_3DES
        return encryption_mode
      
    def decrypt_chunk_3DES(self, chunk):
        key = '0123456701234567'
        iv = ';;;;;;;;'
        des3 = DES3.new(key, DES3.MODE_CFB, iv)

        if len(chunk) == 0:
          print "empty chain"
        return des3.decrypt(chunk)
    
    def decrypt_chunk_AES(self, chunk):
        decoded_encrypted_data = b64decode(chunk)
        decrypted_data = self.key_AES.decrypt(decoded_encrypted_data)
        decrypted_stripped = self.StripPadding(decrypted_data, INTERRUPT, PAD)
        return b64decode(decrypted_stripped)
  
    def StripPadding(self, data, interrupt, pad):
        return data.rstrip(pad).rstrip(interrupt)
      
    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        
        #### direct conversion to CV2 ####
        if (self.enc_mode == MODE_3DES):
          ros_data.data = self.decrypt_chunk_3DES(ros_data.data)
        elif (self.enc_mode == MODE_AES):
          ros_data.data = self.decrypt_chunk_AES(ros_data.data)

        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
        
        #self.fps.update()
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(image_np,"{:.2f}".format(self.fps.partialfps()),(10,470), font, 1,(255,255,255),2) 
        #cv2.imshow('After_Encryption', image_np)
        cv2.imshow('After_Encryption')
        cv2.waitKey(2)

    def exit(self):
        # stop the timer and display FPS information
        #self.fps.stop()
        print("[INFO] Decrypter node: elapsed time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] Decrypter node: approx. FPS: {:.2f}".format(self.fps.fps()))


def main(args):
    '''Initializes and cleans up ros node'''
    rospy.init_node('image_feature', anonymous=True)
    ic = image_feature()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()
    ic.exit()

if __name__ == '__main__':
    #time.sleep( 3 )
    main(sys.argv)
    