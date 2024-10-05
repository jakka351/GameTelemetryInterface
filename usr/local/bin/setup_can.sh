#!/bin/bash

# Bring down any existing CAN interfaces
sudo ip link set can0 down
sudo ip link set can1 down

# Set up CAN interfaces
sudo ip link set can0 type can bitrate 500000
sudo ip link set can1 type can bitrate 125000

# Bring up CAN interfaces
sudo ip link set can0 up
sudo ip link set can1 up
