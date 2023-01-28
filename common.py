import random
from time import sleep
import base64
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def file_json_read(my_path):
    with open(my_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def dir_create_if_not_exists(my_path):
    if os.path.exists(my_path):
        return
    else:
        os.makedirs(my_path)

def http_get_cached(url, file_extension='.htm', decode_response=True, cached_path = 'cached_websites'):
    factor = 1000
    sleep_time = random.randrange(5 * factor, 10  * factor) / factor

    encoded = base64.b64encode(url.encode()).decode()
    encoded_path = os.path.join(cached_path, encoded + file_extension)

    dir_create_if_not_exists(cached_path)

    if not os.path.exists(encoded_path):
        print(f'downloading {url} to {encoded_path}')
        print(f'Sleeping for {sleep_time}s')
        sleep(sleep_time)
        http_get_save(url, encoded_path, decode_response)

    with open(encoded_path, 'r') as opened:
        body = opened.read()
        return body

def http_get_save(url, path_save, decode_response=True):
    with urlopen(url) as response:
        body = response.read()
        if decode_response:
            body = body.decode()
        with open(path_save, 'wb') as f:
            f.write(body)
