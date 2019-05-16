from dlm.ocean import OceanAgent
import os

# Pytest is called from the root directory, so the path to config is from there
oa = OceanAgent('./dlm/config.ini')

def test_get_account():
    assert len(oa.get_account().__dict__) == 2
    assert len(oa.get_account().address) == 42

def test_search():
    random = os.urandom(32)
    assert oa.search(random) == []
