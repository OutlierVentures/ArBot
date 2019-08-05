from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent


class ArBot(FetchAgent, OceanAgent):

    def arb_terms(self, terms):
        return True


if __name__ == '__main__':

    ab = ArBot()
    print('ArBot not ready for use yet.')