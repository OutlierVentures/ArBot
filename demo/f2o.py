'''
This demo shows an example flow of data liquidity: Fetch to Ocean.
Spin the Ocean to Fetch demo up then run this one for a full flow Ocean -> Fetch -> Ocean.
'''

from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent

fa = FetchAgent('Consumer', '127.0.0.1', 10000)
fa.connect()
fa.search('flowers', 0, './purchased.json')
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

oa = OceanAgent('../dlm/config.ini')
oa.publish('Iris Dataset',
           'Multivariate Iris flower dataset for linear discriminant analysis.',
           0,
           'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
           'CCO: Public Domain',
           ['flowers', 'classification', 'plants'])
