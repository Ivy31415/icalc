from dataclasses import dataclass
from enum import Enum
from typing import Literal, Union
from tokenizer import *

class BinaryOp(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

class Node:
    def eval(self):
        return 0

@dataclass
class LiteralNode(Node):
    num:Union[int,float]

    def eval(self):
        return self.num

@dataclass
class BinaryOpNode(Node):
    left:Node
    op:BinaryOp
    right:Node

    def eval(self):
        l = self.left.eval()
        r = self.right.eval()
        if self.op == BinaryOp.ADD:
            return l + r
        if self.op == BinaryOp.MUL:
            return l * r
        if self.op == BinaryOp.SUB:
            return l - r
        if self.op == BinaryOp.DIV:
            return l / r

def oper_token_to_enum(oper:Token) -> BinaryOp:
    assert oper.variant == TokenVariant.OPER
    if oper.value == '*':
        return BinaryOp.MUL
    if oper.value == '+':
        return BinaryOp.ADD
    if oper.value == '-':
        return BinaryOp.SUB
    if oper.value == '/':
        return BinaryOp.DIV

def make_literal_node(arg:Token) -> LiteralNode:
    assert arg.variant == TokenVariant.NUM
    return LiteralNode((float if '.' in arg.value else int)(arg.value))

def make_binary_node(left:Node, oper:Token, right:Node) -> BinaryOpNode:
    assert oper.variant == TokenVariant.OPER
    return BinaryOpNode(left, oper_token_to_enum(oper), right)
     

def parse(tokens:List[Token]) -> Node:
    assert len(tokens) % 2 == 1

    result:Node = make_literal_node(tokens.pop(0))

    while tokens:
        oper = tokens.pop(0)
        num = make_literal_node(tokens.pop(0))
        result = make_binary_node(result, oper, num)

    return result