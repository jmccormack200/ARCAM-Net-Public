#!/usr/bin/env bash

##Now we will download gr-mac
cd ..
cd ..
git clone https://github.com/balint256/gr-mac.git
cd gr-mac
mkdir build
cd build
cmake ..
sudo make
sudo make install

sudo ldconfig

##Which also needs gr-foo
cd ..
cd ..
git clone https://github.com/bastibl/gr-foo.git
cd gr-foo
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig


#RTL Driver
cd ..
cd ..
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
sudo make
sudo make install
sudo ldconfig

#RTL-GNU Radio Pluging
cd ..
cd ..
git clone git://git.osmocom.org/gr-osmosdr
cd gr-osmosdr/
mkdir build
cd build/
cmake ../
make
sudo make install
sudo ldconfig


cd ..
cd ..
git clone https://github.com/btrowbridge/alfred-ubuntu.git
cd alfred-ubuntu
sudo bash ubuntuAlfredInstall.sh
