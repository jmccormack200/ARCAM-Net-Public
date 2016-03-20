# Tools Folder

## UDP

These are two small scripts I set up in python, useful for testing the network by sending and receiving unique data through UDP. Not super important, but may help.

## tmux_start

To use this file, simply change the IP Addresses to match your setup. You can add as many as you like. In its current state, this will scale up to 255 nodes just fine, but could be edited to handle more if someone needed it to. Your computer must have sshpass on it and it tends to work better if someone already used ssh to connect to the computers before (to handle the key exchange). 

## batman_monitor.sh

This was an attempt at making a script to run batctl on each computer and display it in a single window, still working at this one though. 

## grc_block_install.sh

If you do not want to run the entirety of my GNU Radio Installer, this is the script that will still automatically download and configure the GRC dependencies.

