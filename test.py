from  selenium import webdriver
from bs4 import BeautifulSoup
import requests
import m3u8
from utils import get_master_m3u8, get_url_for_m3u8_file_video, get_sequence_number, get_highest_quality_video
from selenium.webdriver.chrome.options import Options
import time
from celery import Celery

app = Celery(__name__,
             broker="redis://localhost:6379")


@app.task
def save_video(url, filename):
    f = open(filename, 'wb')
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    sec = 0
    current_sequence_number = ''
    url = url
    browser = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    browser.get(url)
    htmldata = browser.page_source
    browser.close()
    soup = BeautifulSoup(htmldata, 'html.parser')
    res = soup.find_all(name='script', attrs={'type': "text/javascript"})
    try:
        response = requests.get(get_master_m3u8(res))
    except:
        return
    m3u8_obj = m3u8.parse(response.text)

    # call a funtion which return higest quality image
    #a = m3u8_obj['playlists'][0]['uri']
    a = get_highest_quality_video(m3u8_obj['playlists'])
    url = get_url_for_m3u8_file_video(a)
    print('downloading started..........')
    while True:
        try:
            datachunks = requests.get(url)
        except:
            f.close()
            return
        vide = m3u8.parse(datachunks.text)
        for i, segment in enumerate(vide['segments']):
            if current_sequence_number == '':
                current_sequence_number = get_sequence_number(segment['uri'])
            #save file here
                try:
                    res = requests.get(get_url_for_m3u8_file_video(segment['uri']), stream=True)
                except:
                    f.close()
                    return
                for chk in res.iter_content(1024):
                    if chk:
                        f.write(chk)
                sec = sec + 1

            seq = get_sequence_number(segment['uri'])
            if current_sequence_number < seq:
                try:
                    res = requests.get(get_url_for_m3u8_file_video(segment['uri']),stream=True)
                except:
                    f.close()
                    return
                for chk in res.iter_content(1024):
                    if chk:
                        f.write(chk)
                sec = sec + 1
            #save to file
                current_sequence_number = seq
                #print('vdo duration now {}..'.format(sec*2))
            # hyperparameter change according to resolution of videos.
            time.sleep(.200)

