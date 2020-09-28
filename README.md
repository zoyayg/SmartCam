# SmartCam

SmartCam is an Artificial Intelligence powered security camera that detects motion, snaps a picture, uses IBM Watson Visual Recognition to detect the person on camera, and then announces them to the owner. Ultimately, if this system is connected to the smart home hub, the owner can control the behavior of the smart appliances dependent upon who is approaching the house.

SmartCam is an open source project written in Python3 and is built on Raspberry Pi.

# This project uses:

- Raspberry Pi 4
- Raspberry Pi Camera Module V2
- Speaker module (any speaker with an audio jack works)
- Python 3
- IBM Watson Visual Recognition API
- IBM Watson Text to Speech

# IBM Watson Services

In order for the code to run you need an active IBM cloud account to run the Watson services. You can create a free account using the link below:
https://www.ibm.com/cloud
After creating IBM cloud ID, log in and activate "Watson Visual Recognition" and "Watson Text to Speech" services. You can use the free version for the purpose of this project - select the Lite version for both services.

After activating the services, note your API Key and URL for each service. you will need them to connect to the services using the API commands in the code.

# Future Work

This project can be scaled to integrate with the smart home appliances already in place. It can also be scaled to have a full conversation with the owner using IBM Watson Assistant. To do so, we need a microphone module for the Raspberry Pi and an active Watson Assistant service. 

This project was part of the IBM Summit Technical Showcase in Summer 2020, and it was awarded first place at the showcase.  

**Please Fork the project if you wish to expand the scope or contribute to it.
