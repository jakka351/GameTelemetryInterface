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
import ctypes
import socket
import struct
import can
import time
import queue
import thraeding
from threading import Thread
import sys, traceback
# we want this lib installed on the RPI as well -  pip install acudpclient
#from acudpclient.client import ACUDPClient

# data byte variables
engineRevolutionsPerMinute = 0
vehicleKilometresPerHour = 0
cylinderHeadTemperature = 0
odometerCount = 0
engineSpeedRateOfChange1 = 0
engineSpeedRateOfChange2 = 0
throttlePositionManifold = 0
throttlePositionRateOfChange = 0
#can ID variables
powertrainControlModule0 = 0x207 
powertrainControlModule01 = 0x44D 
torqueReductionRequest = 0x120
engineSpeedRateOfChange = 0x12D
antiLockBrakeSystem = 0x210
transmissionControlModule = 0x230
frontDisplayInterfaceModule = 0x307
restraintsControlModule = 0x340
restraintsControlModule2 = 0x350
hvacIntegratedModule = 0x353
bodyElectronicModule = 0x403
powertrainControlModule = 0x425
powertrainCOntrolModule2 = 0x427
instrumentCluster = 0x437
powertrainControlModule3 = 0x453
powertrainControlModule4 = 0x454
powertrainControlModule5 = 0x4C0
powertrainControlModule6 = 0x623
powertrainControlModule7 = 0x640
powertrainControlModule8 = 0x650
IC_DiagSig_Rx = 0x720
IC_DiagSig_Tx = 0x728
# AC Telemetry Documentation
# https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub
# AC server IP and port
AC_SERVER_IP = '127.0.0.1'  # Replace with the actual IP if needed
AC_SERVER_PORT = 9996
# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)  # Set a timeout for blocking socket operations
# Struct formats
handshake_format = '<iii'  # Little-endian, 3 integers
handshake_response_format = '<50s50sii50s50s'  # Little-endian, specified types
# Define the RTCarInfo struct using ctypes
class RTCarInfo(ctypes.Structure):
    _fields_ = [
        ('identifier', ctypes.c_char),
        ('size', ctypes.c_int),
        ('speed_Kmh', ctypes.c_float),
        ('speed_Mph', ctypes.c_float),
        ('speed_Ms', ctypes.c_float),
        ('isAbsEnabled', ctypes.c_bool),
        ('isAbsInAction', ctypes.c_bool),
        ('isTcInAction', ctypes.c_bool),
        ('isTcEnabled', ctypes.c_bool),
        ('isInPit', ctypes.c_bool),
        ('isEngineLimiterOn', ctypes.c_bool),
        ('accG_vertical', ctypes.c_float),
        ('accG_horizontal', ctypes.c_float),
        ('accG_frontal', ctypes.c_float),
        ('lapTime', ctypes.c_int),
        ('lastLap', ctypes.c_int),
        ('bestLap', ctypes.c_int),
        ('lapCount', ctypes.c_int),
        ('gas', ctypes.c_float),
        ('brake', ctypes.c_float),
        ('clutch', ctypes.c_float),
        ('engineRPM', ctypes.c_float),
        ('steer', ctypes.c_float),
        ('gear', ctypes.c_int),
        ('cgHeight', ctypes.c_float),
        ('wheelAngularSpeed', ctypes.c_float * 4),
        ('slipAngle', ctypes.c_float * 4),
        ('slipAngle_ContactPatch', ctypes.c_float * 4),
        ('slipRatio', ctypes.c_float * 4),
        ('tyreSlip', ctypes.c_float * 4),
        ('ndSlip', ctypes.c_float * 4),
        ('load', ctypes.c_float * 4),
        ('Dy', ctypes.c_float * 4),
        ('Mz', ctypes.c_float * 4),
        ('tyreDirtyLevel', ctypes.c_float * 4),
        ('camberRAD', ctypes.c_float * 4),
        ('tyreRadius', ctypes.c_float * 4),
        ('tyreLoadedRadius', ctypes.c_float * 4),
        ('suspensionHeight', ctypes.c_float * 4),
        ('carPositionNormalized', ctypes.c_float),
        ('carSlope', ctypes.c_float),
        ('carCoordinates', ctypes.c_float * 3)
    ]

def send_handshake():
    identifier = 1  # As per documentation
    version = 1     # As per documentation
    operation_id = 0  # HANDSHAKE operation
    handshake_data = struct.pack(handshake_format, identifier, version, operation_id)
    sock.sendto(handshake_data, (AC_SERVER_IP, AC_SERVER_PORT))
    print('Handshake request sent.')

def receive_handshake_response():
    try:
        data, addr = sock.recvfrom(4096)  # Buffer size of 4096 bytes
        response = struct.unpack(handshake_response_format, data)
        car_name = response[0].decode('utf-8').rstrip('\x00')
        driver_name = response[1].decode('utf-8').rstrip('\x00')
        identifier = response[2]
        version = response[3]
        track_name = response[4].decode('utf-8').rstrip('\x00')
        track_config = response[5].decode('utf-8').rstrip('\x00')
        print('Handshake response received:')
        print(f'Car Name: {car_name}')
        print(f'Driver Name: {driver_name}')
        print(f'Identifier: {identifier}')
        print(f'Version: {version}')
        print(f'Track Name: {track_name}')
        print(f'Track Config: {track_config}')
        send_scrolling_text('Handshake response received:')
        send_scrolling_text(f'Car Name: {car_name}')
        send_scrolling_text(f'Driver Name: {driver_name}')
        send_scrolling_text(f'Identifier: {identifier}')
        send_scrolling_text(f'Version: {version}')
        send_scrolling_text(f'Track Name: {track_name}')
        send_scrolling_text(f'Track Config: {track_config}')
    except socket.timeout:
        print('Timeout waiting for handshake response.')
        return False
    return True

def subscribe_to_updates():
    identifier = 1  # As per documentation
    version = 1     # As per documentation
    operation_id = 1  # SUBSCRIBE_UPDATE operation
    subscribe_data = struct.pack(handshake_format, identifier, version, operation_id)
    sock.sendto(subscribe_data, (AC_SERVER_IP, AC_SERVER_PORT))
    print('Subscribed to telemetry updates.')
    send_scrolling_text('Subscribed to telemetry updates.')

def receive_telemetry_data():
    global highSpeedCan, MidSpeedCan
    try:
        while True:
            allIsWellOnTheCanBus()
            data, addr = sock.recvfrom(2048)  # Adjust buffer size if needed
            if data:
                identifier = data[0:1].decode('utf-8')
                if identifier == 'a':
                    # Parse RTCarInfo
                    rt_car_info = RTCarInfo.from_buffer_copy(data)
                    # Access the telemetry data
                    print(f"Speed (Km/h): {rt_car_info.speed_Kmh}")
                    print(f"RPM: {rt_car_info.engineRPM}")
                    print(f"Gear: {rt_car_info.gear}")
                    print(f"Lap Time: {rt_car_info.lapTime}")
                    control_tachometer_and_speedometer(int({rt_car_info.engineRPM}), int ({rt_car_info.speed_Kmh}))
                    #ontrol_temp_gauge(int(cylinderHeadTemperature))
                    send_scrolling_text(f"Speed (Km/h): {rt_car_info.speed_Kmh}")
                    send_scrolling_text(f"RPM: {rt_car_info.engineRPM}")
                    send_scrolling_text(f"Gear: {rt_car_info.gear}")
                    send_scrolling_text(f"Lap Time: {rt_car_info.lapTime}")
                    # You can add more fields to display as needed
    except Exception as e:
        print(f'Error receiving telemetry data: {e}')

def send_dismiss():
    identifier = 1  # As per documentation
    version = 1     # As per documentation
    operation_id = 3  # DISMISS operation
    dismiss_data = struct.pack(handshake_format, identifier, version, operation_id)
    sock.sendto(dismiss_data, (AC_SERVER_IP, AC_SERVER_PORT))
    print('Sent dismiss message.')

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
                   ::,,,,,,:~::,~+I+,..~::::::,,,,,,,,,,,,,,,,,~==~~~.........+.......,:,,    ''')
        
def setup():
    global highSpeedCan, MidSpeedCan
    try:
        highSpeedCan = can.interface.Bus(channel='can0', bustype='socketcan_native')
        MidSpeedCan = can.interface.Bus(channel='can1', bustype='socketcan_native')
        # Light Up Cluster on Startup
        MidSpeedCan.send(can.Message(arbitration_id=720, data=[0x02, 0x10, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False))
        MidSpeedCan.send(can.Message(arbitration_id=720, data=[0x05, 0x2F, 0x99, 0x59, 0x07, 0xFF, 0x00, 0x00 ],extended_id=False))
        MidSpeedCan.send(can.Message(arbitration_id=720, data=[0x05, 0x2F, 0x71, 0x40, 0x07, 0xFF, 0x00, 0x00 ],extended_id=False))
        MidSpeedCan.send(can.Message(arbitration_id=720, data=[0x05, 0x2F, 0x71, 0x40, 0x07, 0x00, 0x00, 0x00 ],extended_id=False))
        MidSpeedCan.send(can.Message(arbitration_id=720, data=[0x06, 0x2F, 0x61, 0x97, 0x06, 0x10, 0xF0, 0x00 ],extended_id=False))
        """
        byte[] ipcStartUp = new byte[] { 0, 0, ecuRxIdentifier1, ecuRxIdentifier2, 0x2F, 0x99, 0x59, 0x07, 0xFF}; sendPassThruMsg(ipcStartUp);
        byte[] ipcStartUp2 = new byte[] { 0, 0, ecuRxIdentifier1, ecuRxIdentifier2, 0x2F, 0x71, 0x40, 0x07, 0xFF}; sendPassThruMsg(ipcStartUp2);
        byte[] ipcStartUp3 = new byte[] { 0, 0, ecuRxIdentifier1 , ecuRxIdentifier2, 0x2F, 0x71, 0x40, 0x07, 0x00}; sendPassThruMsg(ipcStartUp3);
        byte[] ipcStartUp4 = new byte[] { 0, 0, ecuRxIdentifier1 , ecuRxIdentifier2, 0x2F, 0x61, 0x97, 0x06, 0x10, 0xF0}; sendPassThruMsg(ipcStartUp4);
        """
    except OSError:
        sys.exit() # quits if there is no canbus interface
    print("                      ")
    print("        CANbus active on", highSpeedCan, MidSpeedCan)   
    
def cleanline():                      # cleans the last output line from the console
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

def cleanscreen():                    # cleans the whole console screen
    os.system("clear")

# CAN messages to keep cluster happy
def allIsWellOnTheCanBus():
    global highSpeedCan
    msg120 = can.Message(arbitration_id=torqueReductionRequest, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg120)
    msg12D = can.Message(arbitration_id=engineSpeedRateOfChange, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg12D)
    msg210 = can.Message(arbitration_id=antiLockBrakeSystem, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg210)
    msg340 = can.Message(arbitration_id=restraintsControlModule, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg340)
    msg350 = can.Message(arbitration_id=restraintsControlModule2, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg350)
    msg353 = can.Message(arbitration_id=hvacIntegratedModule, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg353)
    msg403 = can.Message(arbitration_id=bodyElectronicModule, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg403)
    msg425 = can.Message(arbitration_id=powertrainControlModule, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg425)
    msg427 = can.Message(arbitration_id=powertrainControlModule2, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg427)
    msg437 = can.Message(arbitration_id=instrumentCluster, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg437)
    msg453 = can.Message(arbitration_id=powertrainControlModule3, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg453)
    msg454 = can.Message(arbitration_id=powertrainControlModule4, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg454)
    msg4C0 = can.Message(arbitration_id=powertrainControlModule5, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg4C0)
    msg623 = can.Message(arbitration_id=powertrainControlModule6, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg623)
    msg640 = can.Message(arbitration_id=powertrainControlModule7, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg640)
    msg650 = can.Message(arbitration_id=powertrainControlModule8, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],extended_id=False)
    highSpeedCan.send(msg640)

def send_can_message(can_id, data):
    global highSpeedCan
    data = data + [0] * (8 - len(data))
    message = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
    try:
        highSpeedCan.send(message)
        print(f"Message sent on {can_interface}: ID={hex(can_id)} Data={data}")
    except can.CanError:
        print(f"Failed to send message on {can_interface}")

def control_tachometer_and_speedometer(rpm, kph):
    #logic to convert the RPM and KPH to Hex CAN Message Bytes
    byte0, byte1 = rpm_to_can_bytes(rpm)
    byte4, byte5 = speed_to_can_bytes(kph)
    data = [byte0, byte1, engineSpeedRateOfChange1, engineSpeedRateOfChange2, byte4, byte5, throttlePositionManifold, throttlePositionRateOfChange]  # High byte, low byte for RPM
    send_can_message(powertrainControlModule0, data)

def control_temp_gauge(degrees):
    data = [degrees]  # High byte, low byte for speed
    send_can_message(powertrainControlModule01, data)

def speed_to_can_bytes(speed_kph):
    """
    Convert vehicle speed in KPH to two CAN data bytes (0-512 KPH).
    The speed is divided by 128 as required, and the result is placed in bytes 4 and 5.
    The resulting two bytes will represent the speed in the format:
    - Byte 4: MSB (most significant byte)
    - Byte 5: LSB (least significant byte)
    :param speed_kph: Vehicle speed in kilometers per hour (KPH).
    :return: Two data bytes as a tuple (byte4, byte5)
    """
    if not (0 <= speed_kph <= 512 * 128):
        raise ValueError("Speed must be in the range 0-65536 KPH")
    # Divide the speed by 128 as per the requirement
    adjusted_speed = int(speed_kph / 128)
    # Convert the adjusted speed to two bytes
    byte4 = (adjusted_speed >> 8) & 0xFF  # Extract the MSB (high byte)
    byte5 = adjusted_speed & 0xFF          # Extract the LSB (low byte)
    return byte4, byte5

def rpm_to_can_bytes(rpm):
    """
    Convert RPM to two CAN data bytes (0-6500 RPM).
    The resulting two bytes will represent RPM in the format:
    - Byte 0: MSB (most significant byte)
    - Byte 1: LSB (least significant byte)
    :param rpm: Engine RPM as a decimal number (0-6500)
    :return: Two data bytes as a tuple (byte0, byte1)
    """
    if not (0 <= rpm <= 6500):
        raise ValueError("RPM must be in the range 0-6500")
    # Convert RPM to its hexadecimal representation in two bytes
    rpm_hex = int(rpm)
    byte0 = (rpm_hex >> 8) & 0xFF  # Extract the MSB (high byte)
    byte1 = rpm_hex & 0xFF         # Extract the LSB (low byte)
    return byte0, byte1

def send_big_text(text):
    # Convert the text to hexadecimal ASCII representation
    hex_data = text.encode('ascii').hex().upper()
    # Calculate the total data length in bytes
    total_data_length = len(hex_data) // 2  # Each byte is represented by two hex characters
    # Prepare the data frames according to ISO-TP protocol
    frames = []
    if total_data_length <= 6:
        # Single Frame (SF)
        pci = '{:02X}'.format(0x00 | total_data_length)
        data = pci + hex_data
        frames.append(data)
    else:
        # First Frame (FF)
        total_length = total_data_length
        pci = '{:02X}{:02X}'.format(0x10 | ((total_length >> 8) & 0x0F), total_length & 0xFF)
        data = pci + hex_data[:(6 * 2)]
        frames.append(data)
        hex_data = hex_data[(6 * 2):]

        # Consecutive Frames (CF)
        sn = 1  # Sequence number starts at 1 and cycles from 0 to 15
        while hex_data:
            pci = '{:02X}'.format(0x20 | (sn & 0x0F))
            frame_data = pci + hex_data[:(7 * 2)]
            frames.append(frame_data)
            hex_data = hex_data[(7 * 2):]
            sn = (sn + 1) % 16  # Sequence number cycles from 0 to 15
    # Send the frames over CAN bus
    for frame in frames:
        # Pad the data to 8 bytes (16 hex characters)
        frame_padded = frame.ljust(16, '0')
        # Convert the hex string to bytes
        data_bytes = bytes.fromhex(frame_padded)
        # Create a CAN message
        message = can.Message(arbitration_id=0x309, data=data_bytes, is_extended_id=False)
        try:
            MidSpeedCan.send(message)
            print(f"Sent: ID=0x{can_id:X}, Data={frame_padded}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")
        time.sleep(0.01)  # Small delay between frames

def send_scrolling_text(text):
    """
    :param text: The text string to display on FDIM as scrolling text
    """
    global MidSpeedCan
    """#!/bin/bash
        while true; do;
         cansend can0 2F5#10264a616b6b6133 
         cansend can0 2F5#21353120736e6966 
         cansend can0 2F5#2266696e67207468 
         cansend can0 2F5#2365206275747473 
        done"""
    # Convert the text to hexadecimal ASCII representation
    hex_data = text.encode('ascii').hex().upper()
    # Calculate the total data length in bytes
    total_data_length = len(hex_data) // 2  # Each byte is represented by two hex characters
    # Prepare the data frames according to ISO-TP protocol
    frames = []
    if total_data_length <= 6:
        # Single Frame (SF)
        pci = '{:02X}'.format(0x00 | total_data_length)
        data = pci + hex_data
        frames.append(data)
    else:
        # First Frame (FF)
        total_length = total_data_length
        pci = '{:02X}{:02X}'.format(0x10 | ((total_length >> 8) & 0x0F), total_length & 0xFF)
        data = pci + hex_data[:(6 * 2)]
        frames.append(data)
        hex_data = hex_data[(6 * 2):]

        # Consecutive Frames (CF)
        sn = 1  # Sequence number starts at 1 and cycles from 0 to 15
        while hex_data:
            pci = '{:02X}'.format(0x20 | (sn & 0x0F))
            frame_data = pci + hex_data[:(7 * 2)]
            frames.append(frame_data)
            hex_data = hex_data[(7 * 2):]
            sn = (sn + 1) % 16  # Sequence number cycles from 0 to 15
    # Send the frames over CAN bus
    for frame in frames:
        # Pad the data to 8 bytes (16 hex characters)
        frame_padded = frame.ljust(16, '0')
        # Convert the hex string to bytes
        data_bytes = bytes.fromhex(frame_padded)
        # Create a CAN message
        message = can.Message(arbitration_id=0x2F5, data=data_bytes, is_extended_id=False)
        try:
            MidSpeedCan.send(message)
            print(f"Sent: ID=0x{can_id:X}, Data={frame_padded}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")
        time.sleep(0.01)  # Small delay between frames

def main(): 
    # Main loop to capture and process UDP telemetry data
    send_handshake()
    if receive_handshake_response():
        subscribe_to_updates()
        # Start receiving telemetry data in a separate thread
        telemetry_thread = threading.Thread(target=receive_telemetry_data)
        telemetry_thread.daemon = True
        telemetry_thread.start()

if __name__ == "__main__":
    cleanscreen()                                                # clean the console screen
    scroll()                                                     # scroll out fancy logo text
    setup()                                                      # set the can interface
    main()       
