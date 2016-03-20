#!/bin/bash

# Requires sshpasss
# sudo apt-get install sshpass

SESSION=$USER

# Function to connect to all sessins
# format should be:
#		connect user pass ip

# To turn on network type:
#	sudo bash tmux_start.sh

# To Stop type:
# 	tmux ls
# Then:
#	sudo tmux kill-session -t <name from above command>

connect(){

	tmux split-window -v

	tmux select-pane -t 0

	ssh="sshpass -p $2 ssh -X $1@192.168.1.$3"
	tmux send-keys "$ssh" C-m
	
	tmux send-keys "echo $pass | sudo -S batctl o -w" C-m
}

user='vtclab'
pass='vtclab'


# IP List
# 192.168.1.100
# 192.168.1.101
# 192.168.1.102
# 192.168.1.106
# 192.168.1.107
# 192.168.1.109

#IP = (100, 101, 102, 106, 107, 109)

IP[0]="100"
IP[1]="101"
IP[2]="102"
IP[3]="106"
IP[4]="107"
IP[5]="109"

# Start Session
tmux -2 new-session -d -s $SESSION

next=0

for ip in "${IP[@]}"
do
	tmux split-window -v
	tmux select-pane -t next

	tmux select-layout even-vertical
	
	connect $user $pass $ip

	next= next + 1
done


# Connect to setup session
tmux -2 attach-session -t $SESSION



