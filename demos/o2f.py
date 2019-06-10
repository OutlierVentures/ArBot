'''
This demo shows an example flow of data liquidity: Ocean to Fetch.
'''

from dlm.ocean import OceanAgent
from dlm.fetch import FetchAgent


oa = OceanAgent('../dlm/config.ini')

# Put the dataset on Ocean to start with. Skip this step and change search term below for existing sets.
oa.publish(name = 'Iris Dataset',
           description = 'Multivariate Iris flower dataset for linear discriminant analysis.',
           price = 0,
           url = 'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
           license = 'CC0: Public Domain',
           tags = ['flowers', 'classification', 'plants', 'outlier ventures'])

# Search for desired sets.
list_of_ddos = oa.search('outlier ventures')
ddo = list_of_ddos[0]

# Consume found set. Mock data consumption while squid-py issue #382 is open.
#path_to_data, _ = oa.consume(ddo)
path_to_data = '../test/data/iris.json'

# Spin up a Fetch agent with our dataset.
fa = FetchAgent('OV_DLM', oef_addr = '127.0.0.1', oef_port = 3333, metadata = oa.get_meta_from_ddo(ddo), path_to_data = path_to_data)
fa.connect()

# Publish to Fetch's OEF.
fa.publish(fa.service)
print('Published to the OEF.')

try:
    fa.run()
finally:
    fa.stop()
    fa.disconnect()

