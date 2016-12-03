ULeRobots TEAM

ROS-cipherer

En la actualidad, una parte importante de los sistemas autónomos utilizados en investigación se construyen 
utilizando el ROS. ROS es un framework distribuido donde algunos nodos publican información que otros nodos 
consumen. Este modelo simplifica el intercambio de datos pero plantea una amenaza importante porque un 
proceso malicioso podría interferir fácilmente las comunicaciones. ROS Cipherer pretende encriptar las 
comunicaciones ROS utilizando algoritmos de cifrado simétrico.

ROS Cipherer permitirá que aquellos nodos que hagan uso de su funcionalidad, puedan cifrar sus salidas. 
En ese caso, será necesario utilizar ROS Cipherer para poder consumir las salidas encriptadas.

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
