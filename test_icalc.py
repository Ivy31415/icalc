from icalc import evaluate

def test_evaluate():
    assert evaluate('3+4') == 7
    assert evaluate('3*4') == 12
    assert evaluate('3-4') == -1
    assert evaluate('9/3') == 3

def test_evaluate_three():
    assert evaluate('3+4+5') == 12

    assert evaluate('3*4*5') == 60

def test_evaluate_mixed_signs():
    assert evaluate('3-4+5') == 4
    assert evaluate('3+4-5') == 2
    