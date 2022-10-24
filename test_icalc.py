from icalc import evaluate
import pytest

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
    
def test_evaluate_simple_parens():
    assert evaluate('(3+4)') == 7
    assert evaluate('(3-4)+5') == 4
    assert evaluate('3-(4+5)') == -6
    
def test_evaluate_nested_parens():
    assert evaluate('(3+4)') == 7
    assert evaluate('((3-4)+5)-6') == -2
    assert evaluate('3-(4+(5-6))') == 0

def test_evaluate_parens_with_different_operators():
    assert evaluate('3-(4/5)-6') == -3.8

def test_disjoint_parens():
    assert evaluate('(3-4) / (5-6)') == 1
    assert evaluate('((3-4)-(5-6)) - ((3/4)+(5/6))') == pytest.approx(-1.5833333333)
    