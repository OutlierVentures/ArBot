from dlm.ocean import OceanAgent
from dlm.utils import Utils
import pytest

# Pytest is called from the root directory, so the path to config is from there
oa = OceanAgent('./dlm/config.ini')
ut = Utils
test_time = ut.get_time()

def test_get_account():
    assert len(oa.get_account().__dict__) == 2
    assert len(oa.get_account().address) == 42

def test_publish():
    created_ddo = oa.publish('Iris Dataset ' + test_time,
                             'Multivariate Iris flower dataset for linear discriminant analysis.',
                             0,
                             'https://datahub.io/machine-learning/iris/r/iris.csv',
                             'CCO: Public Domain',
                             ['flowers', 'classification', 'plants'])
    registered_ddo = oa.assets.resolve(created_ddo.did)
    assert created_ddo.did == registered_ddo.did

def test_search():
    assert oa.search(test_time) != []
    print(oa.search(test_time)[0]._services[0].__dict__, oa.search(test_time)[0]._services[1].__dict__, oa.search(test_time)[0]._services[2].__dict__,)
    assert oa.search('iris') != []

@pytest.mark.skip(reason = "Service Agreement type mismatch in Squid-Py")
def test_consume():
    ddo = oa.search(test_time)[0]
    #oa.accounts.request_tokens(account, 10)
    path_to_data, _ = oa.consume(ddo)
    assert os.path.exists(path_to_data)

def test_get_meta_from_ddo():
    ddo = oa.search('iris')[0]
    meta = oa.get_meta_from_ddo(ddo)
    assert meta['base']['description'] == 'Multivariate Iris flower dataset for linear discriminant analysis.'
    assert len(meta['base']['tags']) == 3

