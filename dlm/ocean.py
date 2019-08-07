from squid_py import Ocean, ConfigProvider, Config
from dlm.utils import Utils
import time, os


class OceanAgent(Ocean):

    # Everything in init belongs to this instance, everything outside to all instances
    def __init__(self, path_to_config):
        ConfigProvider.set_config(Config(path_to_config))
        Ocean.__init__(self)
    
    # Instance methods take self as an argument
    def ocean_get_account(self):
        return self.accounts.list()[0]

    def ocean_search(self, terms):
        list_of_ddos = self.assets.search(terms)
        assets = []
        for ddo in list_of_ddos:
            meta = self.ocean_get_meta_from_ddo(ddo)['base']
            asset = {
                'categories': terms,
                'price': int(meta['price']), # NOTE: encoded as string on Ocean!
                'ids': {
                    'ddo': ddo
                }
            }
            assets.append(asset)
        return assets
    
    def ocean_consume(self, ddo):
        service_agreement_id = self.assets.order(ddo.did, "Access", self.ocean_get_account())
        path_to_data = ''
        attempts = 0
        while not os.path.exists(path_to_data) and attempts < 10:
            try:
                path_to_data = os.path.join(self.config.downloads_path, f'datafile.{ddo.asset_id}.0')
            except:
                attempts += 1
                time.sleep(1)
        return os.listdir(path_to_data), service_agreement_id

    def ocean_publish(self, name, description, price, url, license, tags = ['outlier ventures']):
        account = self.ocean_get_account()
        metadata = {
            'base': {
                'name': name,
                'dateCreated': Utils.get_time(),    
                'author': str(account),
                'license': license,
                'price': str(abs(int(price))),
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
    
    # Note curation data may be of use here in future
    def ocean_get_meta_from_ddo(self, ddo):
        for item in ddo._services:
            if item._type == 'Metadata':
                return item._values['metadata']
        return {}


if __name__ == '__main__':
    oa = OceanAgent('./config.ini')
