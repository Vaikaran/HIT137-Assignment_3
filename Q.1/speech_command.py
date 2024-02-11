import speech_recognition as sr
import math

class SpeechCommand:

    def record_speech(self, speech_duration: int):
        with sr.Microphone() as source:
            r = sr.Recognizer()
            # read the audio data from the default microphone
            print("Speak...")
            return r.record(source, duration=speech_duration)      

    def recognize_speech(self, audio_data: any):
        with sr.Microphone() as source:
            r = sr.Recognizer()
            print("Recognizing...")
            # convert speech to text
            try:
                text = r.recognize_google(audio_data)
                print(text)
                return text
            except:
                print('Sorry, Voice command could not be fount!')
                return None
                

    
