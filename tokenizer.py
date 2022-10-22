from enum import Enum
from dataclasses import dataclass
from typing import List

class TokenVariant(Enum):
    UNKNOWN = 0
    NUM = 1
    OPER = 2
    VAR = 3

@dataclass
class Token:
    value:str
    variant:TokenVariant

def tokenize(arg:str) -> List[Token]:

    def is_number_character(value):
        if len(value) > 1:
            return False
        return value[0].isdigit() or value[0] == '.'

    def index_of_next_non_digit(val:str) -> int:
        pos = 0
        while pos < len(val):
            if not is_number_character(val[pos]):
                return pos
            pos += 1
        return len(val)

    def popnextoken(arg2:str) -> Token:
        if arg2[0] in '+-/*^':
            return Token(arg2[0], TokenVariant.OPER)
        if is_number_character(arg2[0]):
            # Find the next index of a NON number character, or -1
            # TODO: Fix the case where there are two decimal symbols in the number.  That should be an error.
            index = index_of_next_non_digit(arg2)
            num = arg2[0:index]
            return Token(num, TokenVariant.NUM) 
        return Token(arg2, TokenVariant.UNKNOWN)

    arg = arg.strip()
    tokens = []
    while arg:
        newtoken = popnextoken(arg)
        arg = arg[len(newtoken.value):].strip()
        tokens.append(newtoken) 
    return tokens
