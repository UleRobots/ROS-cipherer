ULeRobots TEAM

ROS-cipherer

ROS Cipherer se implentará un nuevo nodo ROS, que permitirá que aquellos nodos que hagan uso de su funcionalidad, puedan cifrar sus salidas. En ese caso, será necesario utilizar ROS Cipherer para poder consumir las salidas encriptadas.

The key element trick is to apply pycrypto

sudo apt-get install python-pip
sudo apt-get install autoconf g++ python2.7-dev
sudo apt-get install python-devel
pip  install pycrypto


~/tmp$ pip show pycrypto
---
Name: pycrypto
Version: 2.6.1
Location: /usr/lib/python2.7/dist-packages
Requires: 
