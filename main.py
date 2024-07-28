from time import sleep
import requests
import speech_recognition as sr
from math import *
import re
import pickle
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.driver import get_chrome_driver, wait_for_and_click, wait_for_element
from helpers.utils import transcribe
import helpers.utils
from pydub import AudioSegment
from pydub.silence import split_on_silence
import settings as Config

driver = get_chrome_driver(headless=False)

# login
driver.get('https://unauthorized.tv/account/login/')
wait_for_element(driver, By.XPATH, '//*[@name="username"]').send_keys(Config.unauthorized_username)
wait_for_element(driver, By.XPATH, '//*[@name="password"]').send_keys(Config.unauthorized_password)
wait_for_and_click(driver, By.XPATH, '//button[@type="submit"]')
sleep(5)

transcriptions = [x.split(r'.')[0] for x in os.listdir('./transcriptions/')]
vid_links = helpers.utils.get_video_url_list(driver, 'darkstream')
# list all transcription files in ./transcriptions/
for link in vid_links:
    video_id = link.split('/')[-2]

    # Skip if already transcribed
    if video_id in transcriptions:
        print('Skipping {}'.format(video_id))
        continue
    print('Downloading {}'.format(video_id))
    helpers.utils.download_video_to_mp3(driver, video_id)
    transcribe('downloads/{}.mp3'.format(video_id), 'transcriptions/{}.txt'.format(video_id))

    # Delete the transcript file
    os.remove('downloads/{}.mp3'.format(video_id))