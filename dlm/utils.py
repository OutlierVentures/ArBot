from hashlib import sha256
from datetime import datetime
from urllib.request import urlopen
from requests.exceptions import ConnectionError
import json, requests, os


class Utils:

    @staticmethod
    def get_time():
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def get_remote_hash(url):
        size_limit = 1024 * 1024 * 10
        remote = urlopen(url)
        hash = sha256()
        total_read = 0
        while True:
            data = remote.read(4096)
            total_read += 4096
            if not data or total_read > size_limit:
                break
            hash.update(data)
        return hash.hexdigest()

    @staticmethod
    def load_json(path):
        with open(path) as infile:
            data = json.load(infile)
        return data

    @staticmethod
    def write_json(data, path):
        with open(path, 'w') as outfile:
            json.dump(data, outfile)
    
    @staticmethod
    def site_exists(url):
        if 'file://' in url:
            return True if os.path.exists(url.replace('file://', '')) else False
        else:    
            try:
                requests.get(url)
            except ConnectionError:
                return False
            else:
                return True

