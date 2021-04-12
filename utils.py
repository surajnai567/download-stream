import re


def get_master_m3u8(soup_obj):
    for sc in soup_obj:
        if str(sc).__contains__('var videoconfig'):
            try:
                return re.findall(r'"streamUrl": "(.*)"', str(sc))[0]
            except Exception as e:
                print(e)
                return ''


def get_cid_ecid(m3u8_obj_url):
    return re.findall(r'cid=(\d+)', m3u8_obj_url)


def get_url_for_m3u8_file_video(short_m3u8):
    cid, ecid = get_cid_ecid(short_m3u8)
    base_url = 'https://sportradar-lco-cwpoc.akamaized.net/at/{}/{}/mobile/'.format(cid, ecid)
    return base_url+short_m3u8


def get_sequence_number(st):
    return int(''.join(re.findall('k_(\d*)_(\d*)', st)[0]))


def return_video_id(string:str):
   return string.split('=')[1]


def get_command_for_celery(number_of_process:int):
    return 'celery -A test worker -c {} --loglevel=info -P eventlet'.format(number_of_process)


def check_key(dic: dict, key:str):
    if key in dic.keys():
        return True
    else:
        return False



# write this function for custom video name and resolution
def video_name():
    pass


def _resolution(res:str):
    temp = res.split("x")
    res = int(temp[0]) * int(temp[1])
    return res


def get_highest_quality_video(m3u8_obj):
    current_res = 0
    index = 0
    for i, m3 in enumerate(m3u8_obj):
        temp = m3['stream_info']['resolution']
        if _resolution(temp) > current_res:
            index = i
            current_res = _resolution(temp)
    return m3u8_obj[index]['uri']

