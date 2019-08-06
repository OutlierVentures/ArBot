'''
This demo shows an example flow of data liquidity: Ocean to Fetch.
Spin this up, then spin the Fetch to Ocean demo up for a full flow Ocean -> Fetch -> Ocean.
'''

from dlm.ocean import OceanAgent
from dlm.fetch import FetchAgent

oa = OceanAgent('../dlm/config.ini')
# Put the dataset on Ocean to start with. Skip this step and change search term below for existing sets.
oa.ocean_publish(name = 'Iris Dataset',
                 description = 'Multivariate Iris flower dataset for linear discriminant analysis.',
                 price = 0,
                 url = 'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
                 license = 'CCO: Public Domain',
                 tags = ['flowers', 'classification', 'plants'])
results = oa.ocean_search('flowers')
first_result_ddo = results[0]['ddo']
path_to_data, _ = oa.ocean_consume(first_result_ddo)

fa = FetchAgent()
fa.connect()
fa.fetch_publish_from_ocean_meta(metadata = oa.ocean_get_meta_from_ddo(first_result_ddo),
                                 price = 0,
                                 load_path = path_to_data)
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

