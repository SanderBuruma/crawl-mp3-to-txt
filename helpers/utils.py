import requests
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from math import *
import urllib
import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

import settings as Config
from helpers.driver import get_chrome_driver, wait_for_and_click, wait_for_element

# convert mp3 file to wav  
# show a file dialog box to select a file
def download_video_to_mp3(driver: WebDriver, video_id: str):
    """Go to the video page and download the mp3 from the mp3 link"""
    driver.get('https://unauthorized.tv/video/{}/'.format(video_id))
    link = wait_for_element(driver, By.XPATH, '//*[contains(@href, "mp3")]', 30).get_attribute('href')

    # Download the mp3
    doc = requests.get(link)
    with open('downloads/{}.mp3'.format(video_id), 'wb') as f:
        f.write(doc.content)

def get_video_url_list(driver: WebDriver, channel="darkstream"):
    driver.get('https://unauthorized.tv/channel/{}/'.format(channel))
    return [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//*[contains(@href, "/video/")]')]

def transcribe(src: str, output_file: str = 'temp.txt'):
    l = len(AudioSegment.from_mp3(src))
    divider = 90000
    msg = []
    for i in range(0,l,divider):
        sound = AudioSegment.from_mp3(src)[i:min(i+90000, l-1)]
        print('{0}%'.format(floor(i/l*100)))
        sound.export(r"temp.wav", format="wav")
        sound = AudioSegment.from_wav(r"temp.wav")
        file_audio = sr.AudioFile(r"temp.wav")

        # use the audio file as the audio source                                        
        r = sr.Recognizer()
        
        with file_audio as source:
            audio_text = r.record(source)

            try:
                s = r.recognize_google(audio_text)
                msg.append(s)
                print(s)
            except sr.exceptions.UnknownValueError: pass # There was probably nothing to interpret
            except: pass

    print()
    print(msg)
    # save msg to src.split('.')[0] + '.txt'
    with open(output_file, 'w') as f:
        f.write(' '.join(msg))

if __name__ == '__main__':
    pass