from utils import check_key, return_video_id, get_command_for_celery
from scrapinglivematches import get_all_stream_url
from test import save_video
import time
import os


state = {}
while True:
    url_list = get_all_stream_url()
    for url in url_list:
        if check_key(state, url):
            continue
        print("downloading from....", url)
        file_loc = os.path.join(os.getcwd(), 'videos', "video"+return_video_id(url)+".ts")
        save_video.delay(url, file_loc)
        state[url] = 'active'
    time.sleep(5)

