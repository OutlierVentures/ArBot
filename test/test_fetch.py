from dlm.fetch import FetchAgent
from oef.schema import Description
import pytest

fa = FetchAgent('TestAgent', '127.0.0.1', 3333)

def test_load_service():
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
    service, data = fa.load_service(meta, './test/data/iris_meta.json')
    assert isinstance(service, Description)
    assert isinstance(data, dict)
    with pytest.raises(KeyError):
        fa.load_service({'not': 'valid'}, '/')