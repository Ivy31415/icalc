import tokenizer
import parser

def evaluate(expr:str):
    tokens = tokenizer.tokenize(expr)
    tree = parser.parse(tokens)

    return tree.eval()


if __name__ == "__main__":
    while True:
        expr = input("Enter a string: ")
        print(evaluate(expr))
        