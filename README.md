ROS-cipherer
==============================

More info robotica.unileon.es

## Description
ROS Cipherer permitirá que aquellos nodos que hagan uso de su funcionalidad, puedan cifrar sus salidas. En ese caso, será necesario utilizar ROS Cipherer para poder consumir las salidas encriptadas.

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
