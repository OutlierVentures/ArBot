from dlm.utils import Utils
import os

ut = Utils

def test_get_time():
    time = ut.get_time()
    assert len(time) == 20
    assert time[-1] == 'Z'

def test_get_remote_hash():
    hash = ut.get_remote_hash('https://datahub.io/machine-learning/iris/r/iris.csv')
    assert hash == '69a2774d46b2c322afba26d54109f90ffeeac617b0f771a168d696e66059da6c'

def test_load_json():
    loaded_json = ut.load_json('./test/data/iris_meta.json')
    assert 'base' in loaded_json

def test_write_json():
    temp_path = './test/data/temp.json'
    ut.write_json({'key': 'value'}, temp_path)
    assert os.path.exists(temp_path)
    loaded_json = ut.load_json(temp_path)
    assert 'key' in loaded_json
    os.remove(temp_path)
