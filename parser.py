from dataclasses import dataclass
from enum import Enum
from typing import Literal, Union
from tokenizer import *

class BinaryOp(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

def get_precedence(token:Token) -> int:
    if token.variant == TokenVariant.NUM:
        return 1

    if token.variant == TokenVariant.OPER:
        if token.value in ['+', '-']:
            return 2
        if token.value in ['*', '/']:
            return 3
        raise SyntaxError(f'Unknown operator {token.value}')

    if token.variant in [TokenVariant.OPEN_PAREN, TokenVariant.CLOSE_PAREN]:
        return 4

    raise SyntaxError(f'Token {token.variant} doesnt support the concept of precedence')

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
     

def parse_recursive(tokens:List[Token]) -> Node:
    result:Node = None

    front = tokens[0]

    if front.variant == TokenVariant.OPEN_PAREN:
        # (   <stuff>   )
        # Take the ( off, then recurse.  The return value will tells us where we stopped, which should be a ) that we can just pop
        tokens.pop(0)
        result, tokens = parse_recursive(tokens)
        assert tokens and tokens[0].variant == TokenVariant.CLOSE_PAREN
        tokens.pop(0)   # Remove the close paren
    else:
        assert front.variant == TokenVariant.NUM
        result = make_literal_node(front)
        tokens.pop(0)

    while tokens and tokens[0].variant != TokenVariant.CLOSE_PAREN:
        oper = tokens.pop(0)
        if tokens[0].variant == TokenVariant.NUM:
            right = make_literal_node(tokens.pop(0))
        elif tokens[0].variant == TokenVariant.OPEN_PAREN:
            right, tokens = parse_recursive(tokens)
        result = make_binary_node(result, oper, right)

    return result, tokens

def parse(tokens:List[Token]) -> Node:
    root, remaining = parse_recursive(tokens)

    assert len(remaining) == 0
    return root
    