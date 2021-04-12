from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re

chrome_options = Options()
chrome_options.add_argument("--headless")

current_sequence_number = ''
url = 'https://live.itftennis.com/en/live-streams/'
browser = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
browser.get(url)
htmldata = browser.page_source
browser.close()
soup = BeautifulSoup(htmldata, 'html.parser')
res = soup.find(name='div', attrs={'class': "videos_grid clearfix"})
base_url = "https://live.itftennis.com/"
a_tag = res.find_all(name='a', attrs={'href': re.compile('.*')})


def get_all_stream_url():
    streams = set()
    for tag in a_tag:
        if tag.has_attr('href'):
            streams.add(base_url + tag['href'])

    return list(streams)

