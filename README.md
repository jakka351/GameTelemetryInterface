
<a href="https://testerpresent.com.au/"><img src="https://img.shields.io/badge/Tester Present Specialist Automotive Solutions -Open Source Projects- blue" /></a>

# GameTelemetryInterface
## Get in touch with <a href="https://testerpresent.com.au">Tester Present</a> if you have a project you need help with.


UDP telemetry from video games interfaced to an Instrument Cluster via CANbus

##
Driving an FG Falcon Instrument Cluster with Video Game Telemetry. Basic set up is PC connected via ethernet to Raspberry Pi, which has a SPI>CAN interface attached, thus allowing game telemetry to flow to the RPI via UDP, where software then converts that signal into a CANbus signal and that drives the instrument cluster, giving you a working cluster that is driven from the video game.

##

# Obtaining Telemetry
Using UDP, a python script is able to Handshake with the AC Server to provide it identifiers, followed by subscribing to telemetry updates. The telemetry data can then be recieved in python and manipulated as necessary to data bytes for a CAN message.

# CAN Interface
Raspbery Pi 4 with a PiCAN Dual CAN hat. The pi is setup with socketcan which provides CANbus on can0 and can1 as network interfaces. The script then uses the python-CAN library to interface with socketcan and provide CAN comms.

# Simulator
![image](https://github.com/user-attachments/assets/793c572d-3482-41c1-83b1-e0e08f803cd5)

