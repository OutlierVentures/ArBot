'''
This demo shows an example flow of data liquidity: Fetch to Ocean.
Spin the Ocean to Fetch demo up then run this one for a full flow Ocean -> Fetch -> Ocean.
'''

from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent

fa = FetchAgent()
fa.connect()
fa.fetch_search('flowers')
#search_results = fa.fetch_get_search_results()
fa.fetch_consume(number_to_consume = 1, save_path = './')
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

oa = OceanAgent('../dlm/config.ini')
oa.ocean_publish(name = 'Iris Dataset',
                 description = 'Multivariate Iris flower dataset for linear discriminant analysis.',
                 price = 0,
                 url = 'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
                 license = 'CCO: Public Domain',
                 tags = ['flowers', 'classification', 'plants'])
