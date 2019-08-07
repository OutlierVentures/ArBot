from dlm.arbot import ArBot
from dlm.fetch import FetchAgent
from dlm.ocean import OceanAgent
import pytest, threading, time, os

live = True if os.getenv('NET', '') == 'MAIN' or os.getenv('NET', '') == 'TEST' else False

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

ab = ArBot('./dlm/config.ini', './test/data/', 'file://' + os.getcwd())

def test_get_usd_value():
    assert isinstance(ab.get_usd_value('fetch-ai'), float)
    with pytest.raises(KeyError):
        ab.get_usd_value('fetchai')

@pytest.mark.skipif('live')
def test_arb():   
    thread_one = threading.Thread(target = run_fetch_agent())
    thread_two = threading.Thread(target = run_ocean_agent())
    thread_one.start()
    thread_two.start()
    time.sleep(2)
    assert ab.arb('iris classification')

def run_fetch_agent():
    fa = FetchAgent()
    fa.connect()
    fa.fetch_publish_from_ocean_meta(meta, 0, './data/iris.json')
    try:
        fa.run()
    finally:
        fa.stop()
        fa.disconnect()

def run_ocean_agent():
    oa = OceanAgent('./dlm/config.ini')
    oa.ocean_publish(name = meta['base']['name'],
                     description = meta['base']['description'],
                     price = 100,
                     url = 'https://pkgstore.datahub.io/machine-learning/iris/iris_json/data/23a7b3de91da915b506f7ca23f6d1141/iris_json.json',
                     license = 'CCO: Public Domain',
                     tags = meta['base']['tags'])
