# icalc
This is the first "real" python project i've ever worked on. I decided to make this out of spite, because desmos can't iterate functions. the issue i ran into was while coding the collatz conjecture (or, trying to,) i got the function for it: f(x) = {mod(x, 2) = 1: 3x+1, mod(x, 2) = 0: x/2}. but I was unable to iterate the function until it reached 1. I've always been facinated by said conjecture, and have always wanted to visualize the path it takes from each number. My father is helping me make this, and teaching me python along the way. I wrote every line of code by myself, although my dad would usually have to help me figure out what to write. But he would never tell me exactly what to type, he would only explain what problem we need to solve and how to solve it and I would have to figure out what to write.

The code is split into two major components:

# The tokenizer
The tokenizer splits the input string into a sequence of "tokens". This is helpful because it groups related characters together. For examle if the user types `(3.1415+7)/23` then it would split the string into a list like `[OpenParen, 3.1415, OperatorPlus, 7, CloseParen, OperatorDiv, 23]`. This is easier to work with then a bunch of unrelated characters. Basically the tokenizer figures out where the boundaries of the important parts of the expression are and splits the string at those boundaries.

# The parser
The parser takes the list of tokens and makes a tree data structure. Items in the tree are "nodes" that know how to evaluate themselves. So for example a node which represents a number just evaluates to a number. But a node that represents something like 3+4 would of course add them up. Every equation can be written as a true. For exammple (3+4)-7 can be written as:
```
          Subtract
          /      \
        Add       7
       /   \
      3     4
```

and then to "evaluate" it you just evaluate the top of the tree, and the answer comes out.

The hardest part was the order of operations algorithm. My dad and I couldn't figure out but we did some research online and learned that there is an algorithm for this called the [Precedence Climbing Method](https://en.wikipedia.org/wiki/Operator-precedence_parser#Precedence_climbing_method). Using the pseudocode we were able to implement this algorithm, although I don't really understand how it works.

We plan to contiue working on this to add support for functions, variables, and even graphing. For example, I'd like to one day be able to write `Iterate[Collatz[42], 7]` and have it output the number `2` since applying the Collatz function to the number 42 7 times gives 2 (42 -> 21 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2). But we also don't want to just do this for the collatz conjecture, because it's easy to support any functions we want, so could make a general purpose programmable calculator.
