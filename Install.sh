#!/bin/bash
sudo apt update -y sudo apt upgrade -y
sudo apt install -y can-utils python-can python3-can python3 libsocketcan2 libsocketcan-dev 
echo "appending /etc/modules with can modules"
sudo echo "can" | tee -a /etc/modules
sudo echo "vcan" | tee -a /etc/modules

echo "creating setup_can.sh"
sudo echo "
#!/bin/bash

# Bring down any existing CAN interfaces
sudo ip link set can0 down
sudo ip link set can1 down

# Set up CAN interfaces
sudo ip link set can0 type can bitrate 500000
sudo ip link set can1 type can bitrate 125000

# Bring up CAN interfaces
sudo ip link set can0 up
sudo ip link set can1 up" >> /usr/local/bin/setup_can.sh

echo "creating socketcan service"
sudo echo "
[Unit]
Description=SocketCAN setup for can0 and can1
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/setup_can.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target" >> /lib/systemd/system/socketcan.service

echo "creating telemetry service"
sudo echo "
[Unit]
Description=Telemetry Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/telemetry.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target"

echo 
