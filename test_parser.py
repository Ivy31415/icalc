from parser import *

def ln(value):
    return LiteralNode(value)

def bn(l, op:BinaryOp, r):
    return BinaryOpNode(l, op, r)

def test_literal():
    assert ln(3).eval() == 3
    assert ln(0).eval() == 0

def test_add():
    assert bn(ln(3), BinaryOp.ADD, ln(4)).eval() == 7
    assert bn(ln(3), BinaryOp.ADD, bn(ln(4), BinaryOp.SUB, ln(5))).eval() == 2

def test_parse_literal():
    tokens = tokenize('3')
    assert parse(tokens) == ln(3)

    tokens = tokenize('  3.14  ')
    assert parse(tokens) == ln(3.14)

def test_parse_addition():
    tokens = tokenize('3+4')
    assert parse(tokens) == bn(ln(3), BinaryOp.ADD, ln(4))
    