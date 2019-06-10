from squid_py import Ocean, ConfigProvider, Config
from dlm.utils import Utils
import datetime, os


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
            'base': {
                'name': name,
                'dateCreated': Utils.get_time(),    
                'author': str(account),
                'license': license,
                'price': str(price),
                'files': [
                    {
                        'index': 0,
                        'checksum': Utils.get_remote_hash(url),
                        'checksumType': 'SHA-256',
                        'url': url
                    }
                ],
                'tags': tags,
                'type': 'dataset',
                'description': description
            }
        }
        ddo = self.assets.create(metadata, account)
        # Ensure asset registered successfully before returning
        registered_ddo = self.assets.resolve(ddo.did)
        assert ddo.did == registered_ddo.did
        return ddo

    def search(self, terms):
        list_of_ddos = self.assets.search(terms)
        return list_of_ddos
    
    def consume(self, ddo):
        service_agreement_id = self.assets.order(ddo.did, 0, self.get_account())
        path_to_data = ''
        attempts = 0
        while not os.path.exists(path_to_data) and attempts < 10:
            try:
                path_to_data = os.path.join(ConfigProvider.get_config().downloads_path, f'datafile.{ddo.asset_id}.0')
            except:
                attempts += 1
                time.sleep(1)
        return os.listdir(path_to_data), service_agreement_id
    
    # Note curation data may be of use here in future
    def get_meta_from_ddo(self, ddo):
        for item in ddo._services:
            if item._type == 'Metadata':
                return item._values['metadata']
        return {}



if __name__ == '__main__':
    oa = OceanAgent('./config.ini')
