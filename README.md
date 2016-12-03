ROS-cipherer
==============================

## Description
ROS Cipherer permitirá que aquellos nodos que hagan uso de su funcionalidad, puedan cifrar sus salidas. En ese caso, será necesario utilizar ROS Cipherer para poder consumir las salidas encriptadas.

## Environment settings
It is necessary to have Ubuntu 14.04 and ROS (Indigo version) installed.
#### Steps to install ROS indigo
Setup your computer to accept software from packages.ros.org

      $ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
-------
      $ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116      

Then, make an update:

      $ sudo apt-get update
      
For a complete installation of ROS (recommended):

      $ sudo apt-get install ros-indigo-desktop-full
      
It's convenient if the ROS environment variables are automatically added to your bash session every time a new shell is launched: 

      $ echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
      $ source ~/.bashrc
      
Now, it is also necessary to configuring the workspace:
Let's create a catkin workspace: 

      $ mkdir -p ~/catkin_ws/src
      $ cd ~/catkin_ws/src
      $ catkin_init_workspace
      
To build de workspace:

      $ cd ~/catkin_ws/
      $ catkin_make
      
Then:
      
      $ echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
      
*Remember*: After cloning ROS-cipherer proyect on ~/catkin_ws/src and after each modification make, run

      $ catkin_make

For more information about ROS installation, consult the ROS tutorials http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
    

## Dependences
The key element trick is to apply pycrypto

      $ sudo apt-get install python-pip autoconf g++ python2.7-dev python-devel
      $ pip  install pycrypto
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
      $ roslaunch  simple_talker_listener  talkerCipherer.launch

####PC side:
      $ roslaunch  simple_talker_listener  listenerCipherer.launch


To execute the image ciphering to send images between nodes:
####Robot side:
      $ roslaunch  image_ciphering  image_node_encryption.launch
####PC side:
      $ roslaunch  image_ciphering  image_node_decryption.launch
     
## Crypto algorithms 
 AES y 3DES



More info http://robotica.unileon.es
