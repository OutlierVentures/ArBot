from dlm.fetch import FetchAgent
from oef.schema import Description
from oef.query import Query
from unittest.mock import MagicMock
from typing import List
import pytest, json, os

meta = {
    'base': {
        'name': 'Iris Dataset',
        'description': 'Multivariate Iris flower dataset for linear discriminant analysis.',
        'tags': [
            'flowers',
            'classification',
            'plants'
        ]
    }
}
data_path = './test/data/iris.json'
mock_counterparty = 'alice'

fa = FetchAgent()

# Higher-order helper for functions that need to be online
def online(function):
    def connect_work_disconnect():
        fa.connect()
        function()
        fa.disconnect()
    return connect_work_disconnect

def test_load_service():
    service, data = fa.load_service(meta, data_path)
    assert isinstance(service, Description)
    assert isinstance(data, (dict, List))
    with pytest.raises(KeyError):
        fa.load_service({'not': 'valid'}, '/')

def test_on_message():
    # Mock a search having happened by setting a save_path
    fa.save_path = './test/data/purchased.json'
    dict_from_bytes_sent = fa.on_message(0, 0, mock_counterparty, json.dumps(meta).encode('utf-8'))
    assert dict_from_bytes_sent == meta
    assert os.path.isfile(fa.save_path)
    os.remove(fa.save_path)
    fa.save_path = ''

@online
def test_fetch_publish():
    data = meta['base']
    assert fa.fetch_publish(data['name'],
                            data['description'],
                            0,
                            data_path,
                            data['tags'])

@online
def test_fetch_publish_from_ocean_meta():
    assert fa.fetch_publish_from_ocean_meta(meta, 0, data_path)

@online
def test_on_cfp():
    fa.on_cfp(0, 0, mock_counterparty, 0, Query)

@online
def test_on_accept():
    fa.on_accept(2, 0, mock_counterparty, 2)

def test_on_decline():
    fa.on_decline(2, 0, mock_counterparty, 2)

'''
Note that the OEF module handles the negotiation testing underneath.
For an example negotiation take a look at the demo files o2f.py and f2o.py.
'''
@online
def test_fetch_search():
    fa.fetch_search('flowers', 0, './test/data/purchased.json')
    fa.on_search_result = MagicMock()
    assert fa.on_search_result.assert_called

@online
def test_on_search_result():
    fa.on_search_result(0, [mock_counterparty, 'bob'])
    fa.on_search_result(1, [])

@online
def test_on_propose():
    accepted = fa.on_propose(0, 0, mock_counterparty, 0, [Description({'price': 0})])
    assert accepted == True
    accepted = fa.on_propose(1, 0, mock_counterparty, 0, [Description({'price': 1})])
    assert accepted == False

    
