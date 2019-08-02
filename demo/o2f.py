'''
This demo shows an example flow of data liquidity: Ocean to Fetch.
Spin this up, then spin the Fetch to Ocean demo up for a full flow Ocean -> Fetch -> Ocean.
'''

from dlm.ocean import OceanAgent
from dlm.fetch import FetchAgent

oa = OceanAgent('../dlm/config.ini')
# Put the dataset on Ocean to start with. Skip this step and change search term below for existing sets.
oa.publish('Iris Dataset',
           'Multivariate Iris flower dataset for linear discriminant analysis.',
           0,
           'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
           'CCO: Public Domain',
           ['flowers', 'classification', 'plants'])
list_of_ddos = oa.search('flowers')
ddo = list_of_ddos[0]
# Consume found set. Mock data consumption while squid-py issue #382 is open.
#path_to_data, _ = oa.consume(ddo)
path_to_data = '../test/data/iris.json'

fa = FetchAgent(load_path = path_to_data, metadata = oa.get_meta_from_ddo(ddo))
fa.connect()
fa.publish()
print('Published to the OEF.')
try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

