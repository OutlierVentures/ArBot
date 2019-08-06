from dlm.utils import Utils
import os

ut = Utils()

def test_get_time():
    time = ut.get_time()
    assert len(time) == 20
    assert time[-1] == 'Z'

def test_get_remote_hash():
    hash = ut.get_remote_hash('https://outlierventures.io/wp-content/uploads/2019/05/OV_Sponsor-logos.jpg')
    assert hash == 'b1790a94e8450e171f9a2ed0ad222034622937e14b583cc2d192fc10cc41a526'

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
