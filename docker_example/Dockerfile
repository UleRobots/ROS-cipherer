FROM ubuntu:14.04

MAINTAINER Robotics

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116
RUN apt-get update
RUN apt-get install ros-indigo-desktop-full
RUN apt-get install git-core
RUN apt-get install python-pip
RUN apt-get install autoconf g++ python2.7-dev
RUN apt-get install python-devel
RUN pip install pycrypto

RUN apt-get install python-rosinstall

RUN mkdir -p /catkin_ws/src
RUN cd /catkin_src/src
RUN catkin_init_workspace

RUN catkin_ws/
RUN catkin_make

RUN git clone https://github.com/UleRobots/ROS-cipherer.git

RUN cd /catkin_ws/
RUN catkin_make


