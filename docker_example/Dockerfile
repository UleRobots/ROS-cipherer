FROM ubuntu:14.04

MAINTAINER Robotics

RUN sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116
RUN sudo apt-get update
RUN sudo apt-get install ros-indigo-desktop-full
RUN sudo apt-get install git-core
RUN sudo apt-get install python-pip
RUN sudo apt-get install autoconf g++ python2.7-dev
RUN sudo apt-get install python-devel
RUN pip install pycrypto

RUN sudo apt-get install python-rosinstall

RUN mkdir -p ~/catkin_ws/src
RUN cd ~/catkin_src/src
RUN catkin_init_workspace

RUN ~/catkin_ws/
RUN catkin_make

RUN git clone sudo apt-get install python-rosinstall

RUN ~/catkin_ws/
RUN catkin_make



