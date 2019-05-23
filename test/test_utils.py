from dlm.utils import Utils

ut = Utils

def test_get_time():
    time = ut.get_time()
    assert len(time) == 20
    assert time[-1] == 'Z'

def test_get_remote_hash():
    hash = ut.get_remote_hash('https://datahub.io/machine-learning/iris/r/iris.csv')
    assert hash == '69a2774d46b2c322afba26d54109f90ffeeac617b0f771a168d696e66059da6c'
