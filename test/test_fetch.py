# See Fetch's excellent underlying error handling
from dlm.fetch import FetchAgent
from oef.schema import Description
from oef.query import Query
from unittest.mock import MagicMock
import pytest, json

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
data_path = './test/data/iris_meta.json'
mock_counterparty = 'alice'

fa = FetchAgent(public_key = 'TestAgent',
                oef_addr = '127.0.0.1',
                oef_port = 3333,
                load_path = data_path,
                metadata = meta)

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
    assert isinstance(data, dict)
    with pytest.raises(KeyError):
        fa.load_service({'not': 'valid'}, '/')

def test_on_message():
    dict_from_bytes_sent = fa.on_message(0, 0, mock_counterparty, json.dumps(meta).encode('utf-8'))
    assert dict_from_bytes_sent == meta

@online
def test_publish():
    fa.publish()

@online
def test_on_cfp():
    fa.on_cfp(0, 0, mock_counterparty, 0, Query)

@online
def test_on_accept():
    fa.on_accept(2, 0, mock_counterparty, 2)

def test_on_decline():
    fa.on_decline(2, 0, mock_counterparty, 2)

'''
This is sufficint since it covers the flow within class FetchAgent and OEFProxy handles errors underneath.
NOTE open to PRs writing a test that boots up fetch.py in a subshell and searches for that instance's service.
This is not trivial since these are instance methods - see OEFProxy's on_propose().
'''
@online
def test_search():
    fa.search('flowers')
    fa.on_search_result = MagicMock()
    assert fa.on_search_result.assert_called

@online
def test_on_search_result():
    fa.on_search_result(0, [mock_counterparty, 'bob'])
    fa.on_search_result(1, [])

@online
def test_on_propose():
    # First argument is maximum price for accept
    accepted = fa.on_propose(0, 0, 0, mock_counterparty, 0, [Description({'price': 0})])
    assert accepted == True
    accepted = fa.on_propose(0, 1, 0, mock_counterparty, 0, [Description({'price': 1})])
    assert accepted == False

    
