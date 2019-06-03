from dlm.fetch import FetchAgent
from oef.schema import Description
import pytest

fa = FetchAgent('TestAgent', '127.0.0.1', 3333)

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
