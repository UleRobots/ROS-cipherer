ROS-cipherer
==============================

More info robotica.unileon.es

## Description
ROS Cipherer permitirá que aquellos nodos que hagan uso de su funcionalidad, puedan cifrar sus salidas. En ese caso, será necesario utilizar ROS Cipherer para poder consumir las salidas encriptadas.

## Dependences
The key element trick is to apply pycrypto

      sudo apt-get install python-pip autoconf g++ python2.7-dev python-devel
      pip  install pycrypto
======
      ~/tmp$ pip show pycrypto
======
      Name: pycrypto
      Version: 2.6.1
      Location: /usr/lib/python2.7/dist-packages
      Requires: 

## Instructions to run code:
To execute simple talker/listener to send string messages between ROS nodes in encrypted way:
####Robot side:
      roslaunch  simple_talker_listener  talkerCipherer.launch

####PC side:
      roslaunch  simple_talker_listener  listenerCipherer.launch


To execute the image ciphering to send images between nodes:
####Robot side:
       roslaunch  image_ciphering  image_node_encryption.launch
####PC side:
      roslaunch  image_ciphering  image_node_decryption.launch
     
## Crypto algorithms 
 AES y 3DES
