# GameTelemetryInterface
UDP telemetry from video games interfaced to an Instrument Cluster via CANbus

##
Driving an FG Falcon Instrument Cluster with Video Game Telemetry. Basic set up is PC connected via ethernet to Raspberry Pi, which has a SPI>CAN interface attached, thus allowing game telemetry to flow to the RPI via UDP, where software then converts that signal into a CANbus signal and that drives the instrument cluster, giving you a working cluster that is driven from the video game.

##
# Simulator
![image](https://github.com/user-attachments/assets/793c572d-3482-41c1-83b1-e0e08f803cd5)

