import os

import shutil

import json

from pathlib import Path

from datetime import datetime

from content_classes import Article, QueryPage

def hash_query(*args):
    return(hex(abs(fnv(";".join([*args]))) % (2 ** 32 - 1))[2:])

def fnv(data):
    string = data.lower()
    bstring = string.encode()
    hash = 0x811C9DC5

    for i in range(len(bstring)):
        b = bstring[i]
        hash ^= b
        hash *= 0x100000001b
    return hash

def read_cached(cache_hash):
    cache_paths = get_cache_paths()

    for folder_path in cache_paths:
        for cache_file in folder_path.glob('*'):
            if cache_file.name == (cache_hash + '.json'):
                with open(cache_file, 'r') as file:
                    json_data = file.read()
                #print(cache_file.name)
                return QueryPage.from_json(json_data)
    return None

def get_cache_paths():
    cache_path = Path.home() / '.tearx' / 'cache'

    paths = []

    current_timestamp = datetime.utcnow().replace(year=1)
    for folder_path in cache_path.glob('*'):
        folder_timestamp = unpack_ascii_timestamp(folder_path.name)
        delta_hours = (current_timestamp - folder_timestamp).total_seconds() / 3600 
        if delta_hours > 12:
            remove(folder_path)
        else:
            paths.append(folder_path)

    return paths

def remove(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.islink(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise FileNotFoundError(f"Error: {path} does not exist.")
    except Exception as e:
        print(f"Error occurred while removing {path}: {str(e)}")


def write_cache(hash, content):
    cache_path = Path.home() / '.tearx' / 'cache'
    timestamp = generate_ascii_timestamp(datetime.utcnow())
    folder_path = cache_path / timestamp 
    file_path = folder_path / (hash + '.json')

    folder_path.mkdir(parents=True, exist_ok=True)

    with file_path.open(mode='w') as file:
        file.write(content.dump())

def read_cache(hash):
    return

def generate_ascii_timestamp(timestamp):
    month = chr(ord('a') + int(timestamp.strftime("%m")) - 1)
    day = chr(ord('a') + int(timestamp.strftime("%d")) - 1)
    hour = chr(ord('a') + int(timestamp.strftime("%H")) - 1)
    ascii_timestamp = month + day + hour

    return ascii_timestamp

def unpack_ascii_timestamp(ascii_timestamp):
    month = ord(ascii_timestamp[0]) - ord('a') + 1
    day = ord(ascii_timestamp[1]) - ord('a') + 1
    hour = ord(ascii_timestamp[2]) - ord('a') + 1
    timestamp = datetime(1, month, day, hour)

    return timestamp