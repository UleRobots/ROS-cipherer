ROS-cipherer
==============================

## Description
ROS Cipherer allows ROS publisher nodes to publish encrypted topics. Moreover, it allows ROS suscriber nodes to consume encrypted topics

## Packages
ROS Cipherer includes two packages:

- simple_talker_listener: publishes/consumes std_msgs/String to the topic /chatter.
- image_ciphering: publishes/consumes sensor_msgs/CompressedImages to the topic /output/image_encrypted.

## Environment settings
It is necessary to have Ubuntu 14.04 and ROS (Indigo version) installed.
#### Steps to install ROS indigo
Setup your computer to accept software from packages.ros.org

      $ sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
-------
      $ sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116      

Then, make an update:

      $ sudo apt-get update
      
Do a complete installation of ROS (recommended):

      $ sudo apt-get install ros-indigo-desktop-full
      
Add ROS environment variables to your bash session every time a new shell is launched: 

      $ echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
      $ source ~/.bashrc
      
Now, it is also necessary to configuring the workspace.
Let's create a catkin workspace: 

      $ mkdir -p ~/catkin_ws/src
      $ cd ~/catkin_ws/src
      $ catkin_init_workspace
      
Also, add your own workspace environment to the .bashrc file:

      $ echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
      
Then build the workspace:

      $ cd ~/catkin_ws/
      $ catkin_make
      
Now clone the ROS-ciphered repository into your ~/catkin_ws/src:

      $ git clone https://github.com/UleRobots/ROS-cipherer.git

*Remember*: After cloning ROS-cipherer proyect, you have to run

      $ catkin_make

For more information about ROS installation, follow this ROS tutorial http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
    
## Dependences

Install some dev tools and the pycrypto library:

      $ sudo apt-get install python-pip autoconf g++ python2.7-dev python-devel
      $ pip install pycrypto
      
Check pycripto installation:

      ~/tmp$ pip show pycrypto
      Name: pycrypto
      Version: 2.6.1
      Location: /usr/lib/python2.7/dist-packages
      Requires: 

======
More info: http://robotica.unileon.es
