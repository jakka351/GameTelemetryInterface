#!/bin/bash
# GameTelemetryInterface by jakka351
echo "
             ,777I77II??~++++=~::,,,,::::::::::~~~==+~                                        
           ,IIIIII,IIII+~..,,:,,,,,:~:,,.....,~,,:::~+?+?=                                    
         :=I7777I=IIIIII~...:===,:,=~:,,,,,,::=,,,:::~~:=?===                                 
      ~=,?I?777II7IIIII=~,.,,,,,,,,,,,:,,,,,,::,,,,~:~~~~:~+:~:~                              
      I=I?IIIIII~IIIIIII+:..,,,,,,,,,,,,.,.,,::.,,,,:::~~=~:=+~?~~                            
      I77?+?IIIIIIIII7I7=~,.,,,..,,,,.,.,.......,.,.,.,..,,,:~=~:==~~                         
     +=I7777I?+???IIIIII+=:..,,,,,,,,,,,...,,,,,,,,,,,,..,,,:..:?I7+...,,                     
     +=+=I7777I=~~+~:~IIII~,..,,,,,,,,,,..,,,,,...~+II?I?+?III7IIII777I7=.....                
      ==++++III=~~~::~+I:+?~:.........:+IIIIIIII+=?IIIIIII???????????III7II7I....                 
     ██████   █████  ███    ███ ███████    ████████ ███████ ██      ███████ ███    ███ ███████ ████████ ██████  ██    ██    ██ ███    ██ ████████ ███████ ██████  ███████  █████   ██████ ███████ 
    ██       ██   ██ ████  ████ ██            ██    ██      ██      ██      ████  ████ ██         ██    ██   ██  ██  ██     ██ ████   ██    ██    ██      ██   ██ ██      ██   ██ ██      ██      
    ██   ███ ███████ ██ ████ ██ █████         ██    █████   ██      █████   ██ ████ ██ █████      ██    ██████    ████      ██ ██ ██  ██    ██    █████   ██████  █████   ███████ ██      █████   
    ██    ██ ██   ██ ██  ██  ██ ██            ██    ██      ██      ██      ██  ██  ██ ██         ██    ██   ██    ██       ██ ██  ██ ██    ██    ██      ██   ██ ██      ██   ██ ██      ██      
     ██████  ██   ██ ██      ██ ███████       ██    ███████ ███████ ███████ ██      ██ ███████    ██    ██   ██    ██       ██ ██   ████    ██    ███████ ██   ██ ██      ██   ██  ██████ ███████                                                                                                                                                                                    
     ?I+=~~fg+falcon+video+game+telemetry+interface+by+Jakka351~~::::::::~~~~~~~~~~=~=+?7~:    
       ?+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,,   
        =?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:   
          =?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,:   
           ~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~:   
              ~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,:   
                ~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,   
             ,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,   
              :,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...    
               :,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:    
                 ,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~    
                   ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,"
echo "Game Telemetry Interface Install Script. by Jakka351"

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

echo "appending config.txt with mcp2515 enablers"
sudo echo "
# Enable SPI (required for MCP2515 CAN controllers)
dtparam=spi=on
# CAN interface configuration for MCP2515 on can0 and can1
# Configuration for can0 (MCP2515) on SPI0 CE0 (Chip Enable 0)
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25,spimaxfrequency=1000000
# Configuration for can1 (MCP2515) on SPI0 CE1 (Chip Enable 1)
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=24,spimaxfrequency=1000000" | sudo tee -a /boot/config txt

