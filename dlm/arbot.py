from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent


class ArBot(FetchAgent, OceanAgent):

    def __init__(self, path_to_config):
       #OceanAgent.__init__(self, path_to_config)
       FetchAgent.__init__(self)
       pass

    def arb_terms(self, terms):
        return True

    def arb_f2o(self, terms, price_limit):
        #ocean_demand = self.ocean_search(tersm)
        #self.fetch_search(terms)
        #fetch_supply = self.fetch_get_search_results()
        return True



if __name__ == '__main__':

    ab = ArBot('./config.ini')
    print('ArBot not ready for use yet.')