from dlm.arbot import ArBot
import pytest

ab = ArBot('./dlm/config.ini')

def test_get_usd_value():
    assert isinstance(ab.get_usd_value('fetch-ai'), float)
    with pytest.raises(KeyError):
        ab.get_usd_value('fetchai')

def test_arb_terms():
    assert ab.arb_terms(['iris'])

def test_arb_f20():
    assert ab.arb_f2o(terms = ['iris'], price_limit = 100)