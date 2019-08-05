from dlm.arbot import ArBot

ab = ArBot('./dlm/config.ini')

def test_arb_word():
    assert ab.arb_terms(['iris'])

