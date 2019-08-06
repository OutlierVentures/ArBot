from dlm.arbot import ArBot

ab = ArBot('./dlm/config.ini')

def test_arb_terms():
    assert ab.arb_terms(['iris'])

def test_arb_f20():
    assert ab.arb_f2o(terms = ['iris'], price_limit = 100)