from dataclasses import dataclass
from enum import Enum
from tokenize import TokenInfo
from typing import Literal, Union, Tuple
from tokenizer import *

class BinaryOp(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

class UnaryOp(Enum):
    POS = 0
    NEG = 1
    POS_NEG = 2

def get_precedence(token:Token) -> int:
    # Precedence Table:
    #     3:    ()
    #     2:    */
    #     1:    +-
    #
    if token.variant == TokenVariant.OPER:
        if token.value in ['+', '-']:
            return 1
        if token.value in ['*', '/']:
            return 2
        raise SyntaxError(f'error 1: Unknown operator {token.value}')

    if token.variant in [TokenVariant.OPEN_PAREN, TokenVariant.CLOSE_PAREN]:
        return 3

    if token.variant == TokenVariant.NUM:
        return 4

    raise SyntaxError(f'error 2: Token {token.variant} doesnt support the concept of precedence')

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

@dataclass
class UnaryOpNode(Node):
    op:UnaryOp
    right:Node

    def eval(self):
        inner = self.right.eval()
        if self.op == UnaryOp.NEG:
            return -inner
        if self.op == UnaryOp.POS:
            return inner
        raise SyntaxError("Unsupported unary op")

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

def unary_op_to_enum(oper:Token) -> UnaryOp:
    assert oper.variant == TokenVariant.OPER
    if oper.value == '-':
        return UnaryOp.NEG
    if oper.value == '+':
        return UnaryOp.POS
    
def make_literal_node(arg:Token) -> LiteralNode:
    assert arg.variant == TokenVariant.NUM
    return LiteralNode((float if '.' in arg.value else int)(arg.value))

def make_binary_node(left:Node, oper:Token, right:Node) -> BinaryOpNode:
    assert oper.variant == TokenVariant.OPER
    return BinaryOpNode(left, oper_token_to_enum(oper), right)

def parse_primary(tokens: List[Token]) -> Tuple[Node, List[Token]]:
    if tokens[0].variant == TokenVariant.OPER and tokens[0].value in '-+':
        item = tokens.pop(0)
        op = unary_op_to_enum(item)
        root_node, tokens = parse_primary(tokens)
        return UnaryOpNode(op, root_node), tokens

    if tokens[0].variant == TokenVariant.OPEN_PAREN:
        tokens.pop(0)
        root_node, tokens = parse_expr(tokens)
        if tokens[0].variant !=  TokenVariant.CLOSE_PAREN:
            raise SyntaxError('error 3: unexpected_token')
        tokens.pop(0)
        return root_node, tokens
    if tokens[0].variant == TokenVariant.NUM:
        root_node = make_literal_node(tokens[0])
        tokens.pop(0)
        return root_node, tokens
    raise SyntaxError('error 4: Unexpected_Input')

def peek(tokens: List[Token]) -> Token:
    if not tokens:
        return None
    return tokens[0]

def binary_op_matches_predicate(op:Token, pred) -> bool:
    if not op:
        return False
    if op.variant != TokenVariant.OPER:
        return False
    if op.value not in ['+', '-', '/', '*']:
        return False
    return pred(op)

def parse_expr_1(lhs: Node, tokens: List[Token], min_prec: int) -> Tuple[Node, List[Token]]:
    lookahead = peek(tokens)
    while binary_op_matches_predicate(lookahead, lambda token: get_precedence(token) >= min_prec):
        op = lookahead
        tokens.pop(0)
        rhs, tokens = parse_primary(tokens)
        lookahead = peek(tokens)
        while binary_op_matches_predicate(lookahead, lambda token: get_precedence(token) > get_precedence(op)):
            prec2 = get_precedence(op) + (1 if get_precedence(lookahead) > get_precedence(op) else 0)
            rhs, tokens = parse_expr_1(rhs, tokens, prec2)
            lookahead = peek(tokens)
        lhs =  make_binary_node(lhs, op, rhs)
    return lhs, tokens

def parse_expr(tokens:List[Token]) -> Tuple[Node, List[Token]]:
    root_node, tokens = parse_primary(tokens)
    return parse_expr_1(root_node, tokens, 0)

def parse(tokens:List[Token]) -> Node:
    result, tokens = parse_expr(tokens)
    assert not tokens
    return result
