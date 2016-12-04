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
