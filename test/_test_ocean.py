from dlm.ocean import OceanAgent
from dlm.utils import Utils
from squid_py.ddo.ddo import DDO
import pytest, os

# Pytest is called from the root directory, so the path to config is from there
oa = OceanAgent('./dlm/config.ini')
test_time = Utils.get_time()

def test_ocean_get_account():
    assert len(oa.ocean_get_account().__dict__) == 2
    assert len(oa.ocean_get_account().address) == 42

def test_ocean_publish():
    created_ddo = oa.ocean_publish('Iris Dataset ' + test_time,
                                   'Multivariate Iris flower dataset for linear discriminant analysis.',
                                   0,
                                   'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
                                   'CCO: Public Domain',
                                   ['flowers', 'classification', 'plants'])
    # The assets.resolve(did) registration check is part of the publish function itself
    assert isinstance(created_ddo, DDO)

def test_ocean_search():
    assert oa.ocean_search(test_time) != []
    assert oa.ocean_search('iris') != []

def test_consume():
    ddo = oa.ocean_search(test_time)[0]
    #oa.accounts.request_tokens(account, 10)
    path_to_data, _ = oa.consume(ddo)
    assert os.path.exists(path_to_data)

def test_get_meta_from_ddo():
    ddo = oa.ocean_search('iris')[0]
    meta = oa.get_meta_from_ddo(ddo)
    assert meta['base']['description'] == 'Multivariate Iris flower dataset for linear discriminant analysis.'
    assert len(meta['base']['tags']) == 3

