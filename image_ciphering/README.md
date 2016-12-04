image_ciphering
===============

## Description

This is a simple talker/listener node that publishes/consume sensor_msgs/CompressedImages to the /output/image_encrypted topic.

## Instructions to run the code:

To execute the image ciphering to send images between nodes:

#### Robot side:

      $ roslaunch  image_ciphering  image_node_encryption.launch

#### PC side:

      $ roslaunch  image_ciphering  image_node_decryption.launch
