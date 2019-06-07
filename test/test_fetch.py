from dlm.fetch import FetchAgent
from oef.schema import Description
from oef.query import Query
import pytest

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

fa = FetchAgent('TestAgent', '127.0.0.1', 3333, meta, data_path, 0)

def test_load_service():
    service, data = fa.load_service(meta, data_path)
    assert isinstance(service, Description)
    assert isinstance(data, dict)
    with pytest.raises(KeyError):
        fa.load_service({'not': 'valid'}, '/')

def test_publish():
    service, _ = fa.load_service(meta, data_path)
    fa.connect()
    fa.publish(service)
    fa.disconnect()

def test_on_cfp():
    fa.connect()
    fa.on_cfp(0, 0, mock_counterparty, 0)
    fa.disconnect()

def test_on_accept():
    fa.connect()
    fa.on_accept(2, 0, mock_counterparty, 2)
    fa.disconnect()

def test_on_decline():
    fa.on_decline(2, 0, mock_counterparty, 2)

def test_on_decline():
    fa.on_decline(2, 0, mock_counterparty, 2)


    
