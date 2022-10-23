import pytest
from tokenizer import *

def num(n:int):
    return Token(str(n), TokenVariant.NUM)

def op(op:str):
    return Token(op, TokenVariant.OPER)

def test_literal():
    assert tokenize("1") == [num(1)]

def test_two_literals():
    assert tokenize("1 2") == [num(1), num(2)]

def test_addition():
    assert tokenize("1+2") == [num(1), op('+'), num(2)]

def test_subtraction():
     assert tokenize("1-2") == [num(1), op('-'), num(2)]

def test_external_whitespace():
     assert tokenize("     1+2     ") == [num(1), op('+'), num(2)]

def test_internal_whitespace():
     assert tokenize("1     +     2") == [num(1), op('+'), num(2)]

def test_many_terms():
     assert tokenize("1+2-3*4/5+6-7*8-9/10") == [num(1), op('+'), num(2), op('-'),  num(3), op('*'),  num(4), op('/'), num(5), op('+'), num(6), op('-'), num(7), op('*'), num(8), op('-'), num(9), op('/'), num(10)]

def test_multiple_digit_numbers():
    assert tokenize("10+12") == [num(10), op('+'), num(12)]
    assert tokenize("10.43 + 3.75 ") == [num(10.43), op('+'), num(3.75)]

    assert tokenize("0.43 + 3.75 ") == [num(.43), op('+'), num(3.75)]
    assert tokenize(".43 + 3.75 ") == [Token('.43', TokenVariant.NUM), op('+'), num(3.75)]
