from squid_py import Ocean, ConfigProvider, Config
from dlm.utils import Utils
import datetime


class OceanAgent(Ocean):

    # Everything in init belongs to this instance, everything outside to all instances
    def __init__(self, path_to_config):
        ConfigProvider.set_config(Config(path_to_config))
        Ocean.__init__(self)
    
    # Instance methods take self as an argument
    def get_account(self):
        return self.accounts.list()[0]

    def publish(self, name, description, price, url, license, tags = ['outlier ventures']):
        account = self.get_account()
        metadata = {
            "base": {
                "name": name,
                "dateCreated": Utils.get_time(),    
                "author": str(account),
                "license": license,
                "price": price,
                "files": [
                    {
                        "index": 0,
                        "checksum": Utils.get_remote_hash(url),
                        "checksumType": "SHA-256",
                        "url": url
                    }
                ],
                "tags": tags,
                "type": "dataset",
                "description": description
            }
        }
        ddo = self.assets.create(metadata, account)
        return ddo

    def search(self, terms):
        return self.assets.search(terms)
    

if __name__ == "__main__":
    oa = OceanAgent('./config.ini')
