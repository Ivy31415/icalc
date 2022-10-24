from dataclasses import dataclass
from enum import Enum
from typing import Literal, Union, Tuple
from tokenizer import *

class BinaryOp(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

def get_precedence(token:Token) -> int:
    # Precedence Table:
    #     4:    <Literal>
    #     3:    ()
    #     2:    */
    #     1:    +-
    #
    if token.variant == TokenVariant.OPER:
        if token.value in ['+', '-']:
            return 1
        if token.value in ['*', '/']:
            return 2
        raise SyntaxError(f'Unknown operator {token.value}')

    if token.variant in [TokenVariant.OPEN_PAREN, TokenVariant.CLOSE_PAREN]:
        return 3

    if token.variant == TokenVariant.NUM:
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

def prase_parens_expr(tokens:List[Token]) -> Tuple[Node, List[Token]]:
    # Don't call this function unless your list starts with an open paren.
    assert tokens and tokens[0].variant == TokenVariant.OPEN_PAREN

    # (   <expr>   )
    # Take the ( off, then parse an arbitrary expression.  The return value will tells us where we stopped, which should be a ) that we can just pop
    result, tokens = parse_expr_recursive(tokens[1:])
    assert tokens and tokens[0].variant == TokenVariant.CLOSE_PAREN

    if tokens[0].variant != TokenVariant.CLOSE_PAREN:
        raise SyntaxError(f'Unexpected token {tokens[0]}')
    return result, tokens[1:]

def parse_one_node(tokens:List[Token]) -> Tuple[Node, List[Token]]:
    front = tokens[0]

    if front.variant == TokenVariant.NUM:
        return (make_literal_node(front), tokens[1:])
    elif front.variant == TokenVariant.OPEN_PAREN:
        return prase_parens_expr(tokens)

    raise SyntaxError(f'Unexpected token {front.variant}')

def parse_expr_recursive(tokens:List[Token]) -> Tuple[Node, List[Token]]:
    left:Node = None

    left, tokens = parse_one_node(tokens)

    # Keep chomping tokens until we get something unexpected.  The sequence should be a repeating pattern of the form
    #     <operator> <expr>
    # So consume an operator (which is always exactly one token), then consume an expr by recursing.
    while tokens and (tokens[0].variant == TokenVariant.OPER):
        oper = tokens[0]
        right, tokens = parse_one_node(tokens[1:])
        left = make_binary_node(left, oper, right)

    return left, tokens

def parse(tokens:List[Token]) -> Node:
    root, remaining = parse_expr_recursive(tokens)

    assert len(remaining) == 0
    return root
    