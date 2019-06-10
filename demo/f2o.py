'''
This demo shows an example flow of data liquidity: Fetch to Ocean.
Spin the Ocean to Fetch demo up then run this one for a full flow Ocean -> Fetch -> Ocean.
'''

from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent

# Spin up a plain FetchAgent (not holding a dataset).
fa = FetchAgent('Consumer', oef_addr = '127.0.0.1', oef_port = 3333)

