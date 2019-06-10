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
           url = 'https://datahub.io/machine-learning/iris/r/iris.csv',
           license = 'CC0: Public Domain',
           tags = ['flowers', 'classification', 'plants'])

