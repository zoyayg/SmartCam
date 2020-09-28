import P3picam
import picamera
import json
import time
import os
import subprocess
import webbrowser
#import json from os.path
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
from os.path import join, dirname
from datetime import datetime
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from subprocess import call
from ibm_watson import VisualRecognitionV3
from ibm_watson import AssistantV2
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


MotionState = False

# Change these paths to match your directory
PicPath = ""
AudioPath = ""

def CaptureImage(CurrentTime, PicPath):
    # generate the picture's name
    PicName = CurrentTime.strftime("%Y.%m.%d-%H%M%S") + '.jpg'
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.capture(PicPath + PicName)
    print("have taken a picture")
    return PicName

def GetTime():
    # Fetch the current time
    CurrentTime = datetime.now()
    return CurrentTime

def TimeStamp(CurrentTime, PicPath, PicName):
    # Variable for filepath
    FilePath = PicPath + PicName
    # Create message to stamp on picture
    message = CurrentTime.strftime("%Y.%m.%d- %H:%M:%S")
    # Create command to execute
    TimestampCommand = "/usr/bin/convert " + FilePath + " -pointsize 36 \-fill red -annotate +700+650 '" + message + "' " + FilePath
    # Execute the command
    call([TimestampCommand], shell=True)
    print("We have timestamped our picture")


def Watson_Text2Speech(Text_toConvert):
    # Authentication
    ################### use your API key and URL ###################
    t2s_authenticator = IAMAuthenticator ('')
    text_to_speech = TextToSpeechV1(authenticator = t2s_authenticator)
    text_to_speech.set_service_url('')
    
    # Converting text to speech and play it
    # this procedure saves the audio in audio path under name "Watson_Answer_Speech.wav"
    with open(AudioPath + 'Watson_Answer_Speech.wav', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                Text_toConvert,
                voice = 'en-US_AllisonV3Voice',
                accept = 'audio/wav').get_result().content)
        
        audio_to_play = AudioSegment.from_wav(audio_file.name)
        _play_with_simpleaudio(audio_to_play)


def Watson_VR(PicPath_ToClassify):    
    # Authentication
    ################### use your API key and URL ###################
    vr_authenticator = IAMAuthenticator ('')
    visual_recognition = VisualRecognitionV3(
    version = '',
    authenticator = vr_authenticator)
    
    visual_recognition.set_service_url('')
    # Classify an Image using classifier I defined
    with open(PicPath_ToClassify, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file =images_file,
            threshold='0.6',
            classifier_ids='').get_result() ##### your classifier ID here #####
        
        
        if not classes['images'][0]['classifiers'][0]['classes']:
            class_name = 0
            class_score = 0
            
        else:
            class_name = classes['images'][0]['classifiers'][0]['classes'][0]['class']
            class_score = classes['images'][0]['classifiers'][0]['classes'][0]['score']
            
        return class_name, class_score

while True:  
    MotionState = P3picam.motion()
    print(MotionState)
    if not MotionState:
        # Delay to optimize the loop if no motion is detected
        ## delay for 1 second ##
        time.sleep(1)
        
    else:
        # entering the motion 
        CurrentTime = GetTime()
        PicName = CaptureImage(CurrentTime, PicPath)
        
        Class, Score = Watson_VR (PicPath + PicName)
        
        if Score == 0:
            print("nothing detected")
        elif Score > 0.01 and Score < 0.50:
            print("No one is by the door")
        elif Score >= 0.50 and Score < 0.85:
            print("I think it's", Class, ". Check the pictures I took.")
            Watson_Text2Speech("I think it's"+ Class+ ". Check out the pictures I took.")
            webbrowser.open(PicPath)
            # Sleep for 5seconds ro avoid repeating this info
            time.sleep(5)
        else:
            print("it's" , Class ,". Should I open the door?")
            Watson_Text2Speech(Class + " is at the door!")
            # Sleep for 5seconds ro avoid repeating this info
            time.sleep(5)

 