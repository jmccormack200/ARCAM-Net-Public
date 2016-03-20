#!/bin/sh

sudo modprobe batman-adv
sudo batctl if add tun0
sudo ip link set mtu 1532 dev tun0
#sudo ip link set down tun0
sudo ip link set up tun0
#sudo ip link set down bat0
sudo ip link set up bat0


