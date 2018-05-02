"""
This module should be used like follows. You can run all test via:

python -m doctest -v peg.py

>>> P = Expression('P')
>>> Q = Expression('Q')
>>> a = Terminal('a')
>>> b = Terminal('b')
>>> c = Terminal('c')
>>> P <= a >> P >> b | +c | epsilon
>>> Q <= ~(~a) >> P
>>> Q.consume('aaabbb')
6
>>> Q.consume('accbb')
4
>>> Q.consume('ccc') is None
True
>>> P.consume('d')
0
>>> print(Q.tree.arg.exp)
~(~a) >> P
>>> print(P.tree.arg.exp)
a >> P >> b | +c | epsilon
>>> A = Expression('A')
>>> B = Expression('B')
>>> Q = Expression('Q')
>>> K = Expression('K')
>>> A <= a >> b | a >> A >> b
>>> B <= b >> c | b >> B >> c
>>> K <= a | b | c
>>> Q <= ~(~(A >> ~b)) >> +a >> B >> ~K
>>> Q.consume("aaabbbccc")
9
>>> Q.consume("aaabbbcccc")
>>> Q.consume("aaabbbcc")
>>> Q.consume("abc")
3
"""

from functools import lru_cache
import sys
sys.setrecursionlimit(1000000)

class LeftRecursive(Exception):
    pass

class WrongTerminal(Exception):
    pass

class Node(object):
    """Node represents the element of expression's tree."""
    def __init__(self, expression):
        self.exp = expression

class Expression(object):
    """The class for holding Parsing Expression Grammars."""
    def __init__(self, symbol):
        self.tree = Node(self)
        self.symbol = symbol
    def __le__(self, exp2):
        assert(not hasattr(self.tree, 'arg'))
        self.tree.arg = exp2.tree
    def __arity1(self, symbol):
        new_exp = Expression(symbol)
        new_exp.tree.arg = self.tree
        return new_exp
    def __arity2(self, exp2, symbol):
        assert(isinstance(exp2, Expression))
        new_exp = Expression(symbol)
        new_exp.tree.left = self.tree
        new_exp.tree.right = exp2.tree
        return new_exp
    def __or__(self, exp2):
        return self.__arity2(exp2, '|')
    def __rshift__(self, exp2):
        return self.__arity2(exp2, '>>')
    def __pos__(self):
        return self.__arity1('+')
    def __invert__(self):
        return self.__arity1('~')
    def __str__(self):
        if self.symbol == '|':
            return str(self.tree.left.exp) + " | " + str(self.tree.right.exp)
        elif self.symbol == '>>':
            if self.tree.left.exp.symbol == '|':
                left_side = "(" + str(self.tree.left.exp) + ")"
            else:
                left_side = str(self.tree.left.exp)
            if self.tree.right.exp.symbol == '|':
                right_side = "(" + str(self.tree.right.exp) + ")"
            else:
                right_side = str(self.tree.right.exp)
            return left_side + " >> " + right_side
        elif self.symbol == '+':
            if self.tree.arg.exp.symbol in {'|', '>>', '+', '~'}:
                return "+(" + str(self.tree.arg.exp) + ")"
            else:
                return "+" + str(self.tree.arg.exp)
        elif self.symbol == '~':
            if self.tree.arg.exp.symbol in {'|', '>>', '+', '~'}:
                return "~(" + str(self.tree.arg.exp) + ")"
            else:
                return "~" + str(self.tree.arg.exp)
        else:
            return self.symbol
    def isNonterminal(self):
        return self.symbol not in {'|', '>>', '+', '~'} and not isinstance(self, Terminal)
    def consume(self, word):
        """An implementation of packrat parsing."""
        visited = set()
        length = len(word)

        @lru_cache(maxsize=None)
        def parse(elem, idx):
            if elem.isNonterminal():
                if (elem, idx) in visited:
                    raise LeftRecursive("Left recursive is prohibited: " + elem.symbol)
                else:
                    visited.add((elem, idx))
                return parse(elem.tree.arg.exp, idx)
            if elem is epsilon:
                if idx <= length:
                    return 0
                else:
                    return None
            if isinstance(elem, Terminal):
                if idx < length:
                    return 1 if word[idx] == elem.symbol else None
                else:
                    return None
            if elem.symbol == '>>':
                r1 = parse(elem.tree.left.exp, idx)
                if r1 is None:
                    return None
                r2 = parse(elem.tree.right.exp, idx + r1)
                if r2 is None:
                    return None
                return r1 + r2
            if elem.symbol == '|':
                r1 = parse(elem.tree.left.exp, idx)
                if r1 != None:
                    return r1
                return parse(elem.tree.right.exp, idx)
            if elem.symbol == '~':
                r1 = parse(elem.tree.arg.exp, idx)
                return 0 if r1 is None else None
            if elem.symbol == '+':
                r1 = parse(elem.tree.arg.exp, idx)
                if r1 is None:
                    return None
                r2 = parse(elem, idx + r1)
                return r1 if r2 is None else r1 + r2

        result = parse(self, 0)
        parse.cache_clear()
        return result

class Terminal(Expression):
    """Terminal represents letters and the empty string (epsilon)."""
    def __init__(self, symbol):
        super(Terminal, self).__init__(symbol)
        if len(symbol) > 1 and symbol != "epsilon":
            raise WrongTerminal("A terminal must be single letter.")

epsilon = Terminal('epsilon')
