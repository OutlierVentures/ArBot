from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent
from dlm.utils import Utils
from pycoingecko import CoinGeckoAPI


class ArBot(FetchAgent, OceanAgent, CoinGeckoAPI):

    def __init__(self, path_to_ocean_config, path_to_webserver_root, url_of_hosted_data):
       OceanAgent.__init__(self, path_to_ocean_config)
       FetchAgent.__init__(self)
       CoinGeckoAPI.__init__(self)
       self.path_to_webserver_root = path_to_webserver_root
       self.url_of_hosted_data = url_of_hosted_data

    # Path to webserver root is the base path under which your datasets will be hosted.
    def arb(self, terms):
        ocean_prices = self.ocean_search(terms)
        self.fetch_search(terms)
        fetch_prices = self.fetch_get_search_results()
        fetch_min_price_tokens = fetch_prices[0]['price']
        ocean_min_price_tokens = ocean_prices[0]['price']
        fetch_min_price_usd = fetch_min_price_tokens * self.get_usd_value('fetch-ai')
        ocean_min_price_usd = ocean_min_price_tokens * self.get_usd_value('ocean-protocol')
        # Give a 30c buffer (generous Q3 2019) for fees and market inefficiencies
        if (fetch_min_price_usd > (ocean_min_price_usd + 0.3)):
            print('Executing opportunity: buy Ocean, sell Fetch.')
            try:
                download_path, _ = self.ocean_consume(ocean_prices[0]['ids']['ddo'])
                self.fetch_publish_from_ocean_meta(metadata = self.ocean_get_meta_from_ddo(ocean_prices[0]['ids']['ddo']),
                                                   price = fetch_min_price_tokens - 1,
                                                   load_path = download_path)
            except Exception as e:
                print(e)
                return False
            else:
                return True
        elif (ocean_min_price_usd > (fetch_min_price_usd + 0.3)):
            print('Executing opportunity: buy Fetch, sell Ocean.')
            try:
                dataset_filename = '-'.join(terms) + '.json'
                self.fetch_consume(1, self.path_to_webserver_root + dataset_filename)
                self.ocean_publish(name = ' '.join(terms),
                                   description = 'Dataset sourced from Fetch.AI - contains data about ' + ', '.join(terms),
                                   price = ocean_min_price_tokens - 1,
                                   url = self.url_of_hosted_data + dataset_filename,
                                   license = 'CC-BY 4.0',
                                   tags = terms)
            except Exception as e:
                print(e)
                return False
            else:
                return True
        # Catches equal prices, free on both markets and price difference to small to make profit.
        else:
            print('No arb opportunities. Try arbing different data or wait for markets to change.')
            return False
    
    def get_usd_value(self, name):
        price_dict = self.get_price(ids = name, vs_currencies = 'usd')
        return price_dict[name]['usd']
    
    # WRITEME + WRITETEST
    # Pushes a dataset on A to B where there is no known demand on B. High risk of loss.
    #def arb_with_risk(self, terms):
    #    pass


if __name__ == '__main__':

    ab = ArBot('./config.ini', '/var/www/', 'http://localhost/')
    print('ArBot not ready for use yet.')