simple_talker_listener
======================

## Description

This is a simple talker/listener node that publishes/consume std_msgs/String to the /chatter topic.

## Instructions to run the code:

To execute simple talker/listener to send string messages between ROS nodes in encrypted way:

#### Robot side:

      $ roslaunch  simple_talker_listener  talkerCipherer.launch

#### PC side:

      $ roslaunch  simple_talker_listener  listenerCipherer.launch

## You can change the algorithm used for encryption:

#### Robot side

###### AES encryption (default)

      $ roslaunch  simple_talker_listener  talkerCipherer.launch ciphering:=AES secret_key:=XXX

secret_key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long.

###### 3DES encryption

      $ roslaunch  simple_talker_listener  talkerCipherer.launch ciphering:=AES secret_key:=XXX

secret_key must be 16 or 24 bytes long.

#### PC side:

###### AES encryption (default)

      $ roslaunch  simple_talker_listener  listenerCipherer.launch ciphering:=AES secret_key:=XXX

secret_key must be 16 (AES-128), 24 (AES-192), or 32 (AES-256) bytes long.

###### 3DES encryption

      $ roslaunch  simple_talker_listener  listenerCipherer.launch ciphering:=AES secret_key:=XXX
      
secret_key must be 16 or 24 bytes long.
