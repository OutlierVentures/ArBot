from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent
from pycoingecko import CoinGeckoAPI


class ArBot(FetchAgent, OceanAgent, CoinGeckoAPI):

    def __init__(self, path_to_config):
       #OceanAgent.__init__(self, path_to_config)
       FetchAgent.__init__(self)
       CoinGeckoAPI.__init__(self)
       pass

    def arb_terms(self, terms):
        return True

    def arb_f2o(self, terms, price_limit):
        #ocean_demand = self.ocean_search(tersm)
        #self.fetch_search(terms)
        #fetch_supply = self.fetch_get_search_results()
        return True
    
    def get_usd_value(self, name):
        price_dict = self.get_price(ids = name, vs_currencies = 'usd')
        return price_dict[name]['usd']



if __name__ == '__main__':

    ab = ArBot('./config.ini')
    print('ArBot not ready for use yet.')