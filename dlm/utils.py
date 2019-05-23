from datetime import datetime
from urllib.request import urlopen
from hashlib import sha256

class Utils:

    def get_time():
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

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
