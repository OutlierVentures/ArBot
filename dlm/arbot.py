from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent


class ArBot(FetchAgent, OceanAgent):

    def __init__(self, path_to_config):
       #OceanAgent.__init__(self, path_to_config)
       pass

    def arb_terms(self, terms):
        return True


if __name__ == '__main__':

    ab = ArBot('./config.ini')
    print('ArBot not ready for use yet.')