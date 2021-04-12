from celery import Celery
from  selenium import webdriver
from bs4 import BeautifulSoup
import requests
import m3u8
from utils import get_master_m3u8, get_url_for_m3u8_file_video, get_sequence_number
from selenium.webdriver.chrome.options import Options
import time
from celery import Celery
import requests

app = Celery(__name__,
             broker="redis://localhost:6379")

@app.task
def fun(url):
    while True:
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        browser.get(url)
        htmldata = browser.page_source
        browser.close()
        soup = BeautifulSoup(htmldata, 'html.parser')
        time.sleep(5)
        try:
            requests.get('hejbbjj')
        except:
            return
