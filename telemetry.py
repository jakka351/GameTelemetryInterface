#region Copyright (c) 2024, Jack Leighton
#     __________________________________________________________________________________________________________________
#
#                  __                   __              __________                                      __   
#                _/  |_  ____   _______/  |_  __________\______   \_______   ____   ______ ____   _____/  |_ 
#                \   __\/ __ \ /  ___/\   __\/ __ \_  __ \     ___/\_  __ \_/ __ \ /  ___// __ \ /    \   __\
#                 |  | \  ___/ \___ \  |  | \  ___/|  | \/    |     |  | \/\  ___/ \___ \\  ___/|   |  \  |  
#                 |__|  \___  >____  > |__|  \___  >__|  |____|     |__|    \___  >____  >\___  >___|  /__|  
#                           \/     \/            \/                             \/     \/     \/     \/      
#                                                          .__       .__  .__          __                    
#                               ____________   ____   ____ |__|____  |  | |__| _______/  |_                  
#                              /  ___/\____ \_/ __ \_/ ___\|  \__  \ |  | |  |/  ___/\   __\                 
#                              \___ \ |  |_> >  ___/\  \___|  |/ __ \|  |_|  |\___ \  |  |                   
#                             /____  >|   __/ \___  >\___  >__(____  /____/__/____  > |__|                   
#                                  \/ |__|        \/     \/        \/             \/                         
#                                  __                         __  .__                                        
#                   _____   __ ___/  |_  ____   _____   _____/  |_|__|__  __ ____                            
#                   \__  \ |  |  \   __\/  _ \ /     \ /  _ \   __\  \  \/ // __ \                           
#                    / __ \|  |  /|  | (  <_> )  Y Y  (  <_> )  | |  |\   /\  ___/                           
#                   (____  /____/ |__|  \____/|__|_|  /\____/|__| |__| \_/  \___  >                          
#                        \/                         \/                          \/                           
#                                                  .__          __  .__                                      
#                                       __________ |  |  __ ___/  |_|__| ____   ____   ______                
#                                      /  ___/  _ \|  | |  |  \   __\  |/  _ \ /    \ /  ___/                
#                                      \___ (  <_> )  |_|  |  /|  | |  (  <_> )   |  \\___ \                 
#                                     /____  >____/|____/____/ |__| |__|\____/|___|  /____  >                
#                                          \/                                      \/     \/                 
#                                   Tester Present Specialist Automotive Solutions
#     __________________________________________________________________________________________________________________
#      |--------------------------------------------------------------------------------------------------------------|
#      |       https://github.com/jakka351/| https://testerPresent.com.au | https://facebook.com/testerPresent        |
#      |--------------------------------------------------------------------------------------------------------------|
#      | Copyright (c) 2022/2023/2024 Benjamin Jack Leighton                                                          |          
#      | All rights reserved.                                                                                         |
#      |--------------------------------------------------------------------------------------------------------------|
#        Redistribution and use in source and binary forms, with or without modification, are permitted provided that
#        the following conditions are met:
#        1.    With the express written consent of the copyright holder.
#        2.    Redistributions of source code must retain the above copyright notice, this
#              list of conditions and the following disclaimer.
#        3.    Redistributions in binary form must reproduce the above copyright notice, this
#              list of conditions and the following disclaimer in the documentation and/or other
#              materials provided with the distribution.
#        4.    Neither the name of the organization nor the names of its contributors may be used to
#              endorse or promote products derived from this software without specific prior written permission.
#      _________________________________________________________________________________________________________________
#      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#      INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#      DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#      SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#      SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#      WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#      USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#      _________________________________________________________________________________________________________________
#
#       This software can only be distributed with my written permission. It is for my own educational purposes and  
#       is potentially dangerous to ECU health and safety. Gracias a Gato Blancoford desde las alturas del mar de chelle.                                                        
#      _________________________________________________________________________________________________________________
#
#
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#endregion License
import socket
import struct
import can
import time
import queue
from threading import Thread
import sys, traceback
print('                                  I??+=++=~~~~~~~~~~~?I777IIII??++====~======????+==+==~~~~:::::::::~~~~~~~~~====+==I,     ')
print('                                   ?I+=~~=++~~~~~~~~=?=:+IIIII??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~:    ')
print('                                    ?+=~~~~=++~~~~~+???~=?7II??+++++++==~~:~~~~~~:~~???=+:~~~~~~:::::::::~~~~=++:,.,+=,,   ')
print('                                     =?I+~~~==++~~:+??~====+I?+===+++++==~~~::::::::::~????~~~~~:::::~:~==+:,,,,?..::+=:   ')
print('                                       =?I=~~~==++=+++~==:,~~=+====+++++:,,...:,::~:::::~~~~+~:~~:~~==,.,,.?I~,..::~~=,:   ')
print('                                        ~=+I?=~~=~+++~~=...,~:=+====++?:~+=?I~,I=I??..~III7I:==~,.,,.,,.,,,...::~~++~:~:   ')
print('                                           ~?I+=~~~~+~~~.:+,,,:=+===+++~+==~=+:III=?I?77777I~~~===,,,,.,.,,~~~~=+=~::,,:   ')
print('                                             ~?I+=:~~~~~~,,+:,,+==~+++++,:~~:==,??,:,,=??I++,,,:~===,,,::~~=++=:::~=..,,   ')
print('                                          ,,,,:=+?==~~~~.=:~~,..,=+++++=~:=+=~:.,:,,,,::?=I=:::::+~====++++=~:::?I+?,..,   ')
print('                                           :,,,,~+====~:,,,:=,.,,,~~===~~~,:==~~~~~~:..,,,,,,..,,,~==+++~:,~++I++II?...    ')
print('                                            :,,,,,,+==+,:..:==.:,,~:~~~~~:,,,,:~~~~~~~~=========~++++~,....II+II+?...,:    ')
print('                                              ,,,,,,,++.,,.,,,,=:,,~:::~:::,,,,,,,,,::~~~=====~====~.......?I=I.....,:~    ')
print(' Game Telemetry Interface by Jakka351           ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,    ')        


ENGINE_RPM = 0
VEHICLE_SPEED = 0
COOLANT_TEMPERATURE = 0
ODOMETER_COUNT = 0
# Placeholder CAN IDs for RPM and speed
TACHOMETER_CAN_ID = 0x100  # Placeholder CAN ID for Tachometer
SPEEDOMETER_CAN_ID = 0x101  # Placeholder CAN ID for 
COOLANT_TEMP_CAN_ID = 0x102 
# UDP settings (for example, Project CARS telemetry uses UDP port 5606)
UDP_IP = "0.0.0.0"
UDP_PORT = 5606
# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def scroll():
    #prints logo to console
        print('  ')
        print('''  
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
     ?I+=~~fg+falcon+swc+adapter+??++++===~:~~~~~~~=???=?:=~~~~~::::::::~~~~~~~~~~=~=+?7~:    
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
                   ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,    ''')
        
def setup():
    global bus
 #   os.system("sudo modprobe uinput") 
    try:
        bus1 = can.interface.Bus(channel='can0', bustype='socketcan_native')
        bus2 = can.interface.Bus(channel='can1', bustype='socketcan_native')
    except OSError:
        sys.exit() # quits if there is no canbus interface
    print("                      ")
    print("        CANbus active on", bus1, bus2)   
    
def cleanline():                      # cleans the last output line from the console
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():                    # cleans the whole console screen
    os.system("clear")

def send_can_message(can_id, data):
    data = data + [0] * (8 - len(data))
    message = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
    try:
        bus1.send(message)
        print(f"Message sent on {can_interface}: ID={hex(can_id)} Data={data}")
    except can.CanError:
        print(f"Failed to send message on {can_interface}")

def control_tachometer(rpm):
    data = [rpm // 256, rpm % 256]  # High byte, low byte for RPM
    send_can_message(TACHOMETER_CAN_ID, data)

def control_speedometer(kph):
    data = [kph // 256, kph % 256]  # High byte, low byte for speed
    send_can_message(SPEEDOMETER_CAN_ID, data)

def control_temp_gauge(degrees):
    data = [degrees]  # High byte, low byte for speed
    send_can_message(COOLANT_TEMP_CAN_ID, data)

def main(): 
    # Main loop to capture and process UDP telemetry data
    try:
        while True:
            data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
            # Unpack data (the structure and offsets depend on the game's telemetry format)
            # Example for a custom format (you'll need to adjust this based on your game):
            # RPM and speed might be at different offsets, adjust according to your game's format
            ENGINE_RPM = struct.unpack('f', data[8:12])[0]  # Example: RPM at bytes 8-12
            VEHICLE_SPEED = struct.unpack('f', data[12:16])[0]  # Example: Speed at bytes 12-16
            print(f"Engine RPM: {rpm}, Vehicle Speed: {speed}, Engine Temp: COOLANT_TEMPERATURE" )
            # Send RPM and speed to the CAN bus
            control_tachometer(int(ENGINE_RPM))
            control_speedometer(int(VEHICLE_SPEED))
            control_temp_gauge(int(COOLANT_TEMPERATURE))
            # Optional delay
            time.sleep(0.005)

    except KeyboardInterrupt:

        print("Keyboard Interupt, Exiting...")
        sock.close()

if __name__ == "__main__":
    cleanscreen()                                                # clean the console screen
    scroll()                                                     # scroll out fancy logo text
    setup()                                                      # set the can interface
    main()       
