from peg import *
from peg_common import *
import threading
import sys

class ThreadTest:
    def __call__(self):
        self.MakeTest(self.Case1(), 1)
        self.MakeTest(self.Case2(), 2)
        #self.MakeTest(self.Case3(), 3)
        self.MakeTest(self.Case4(), 4)
        self.MakeTest(self.Case5(), 5)
        self.MakeTest(self.Case6(), 6)
        self.MakeTest(self.Case7(), 7)
        print('ThreadTest done')        

    def Case1(self):
        #Test Case 1
        S = Expression('S')
        a = Terminal('a')
        b = Terminal('b')
        S <= +a >> ~(a | b)
        return S

    def Case2(self):
        #Test Case 2
        S = Expression('S')
        a = Terminal('a')
        b = Terminal('b')
        S <= +(a >> b) >> ~(a | b)
        return S

    def Case3(self):
        #Test Case 3 
        S = Expression('S')
        A = Expression('A')
        B = Expression('B')
        C = Expression('C')
        D = Expression('D')
        a = Terminal('a')
        b = Terminal('b')
        A <= a >> ~a | a >> a >> A
        B <= b >> ~b | b >> b >> B
        C <= a >> A | ~a
        D <= b >> B | ~b
        S <= +(a >> a | b) >> S | A >> D >> S | ~(a | b)
        return S

    def Case4(self):
        #Test Case 4
        S = Expression('S')
        a = Terminal('a')
        b = Terminal('b')
        S <= (+a | epsilon) >> (+((b >> b | b) >> +a) | epsilon) >> (b >> b >> ~(a | b) | b >> ~(a | b) | ~(a | b))
        return S

    def Case5(self):
        #Test Case 5
        S = Expression('S')
        A = Expression('A')
        B = Expression('B')
        a = Terminal('a')
        b = Terminal('b')
        A <= +(a >> a | b >> b) | epsilon
        B <= a >> b | b >> a
        S <= A >> (+(B >> A >> B >> A) | epsilon) >> A >> ~(a | b)
        return S

    def Case6(self):
        #Test Case 6
        S = Expression('S')
        A = Expression('A')
        B = Expression('B')
        a = Terminal('a')
        b = Terminal('b')
        A <= a >> (+(a >> b) | epsilon) >> (b | a >> a)
        B <= b >> (+(b >> a) | epsilon) >> (a | b >> b)
        S <= +(A | B) >> ~(a | b) | ~(a | b)
        return S

    def Case7(self):
        #Test Case 7
        S = Expression('S')
        A = Expression('A')
        B = Expression('B')
        a = Terminal('a')
        b = Terminal('b')
        A <= +a | epsilon
        B <= +b | epsilon
        S <= A >> B >> A >> B >> ~(a | b)
        return S
    
    def TestPositive(self, exp: Expression, word: str):
        if exp.consume(word) is None:
            raise Exception("Consume positive error")
        
    def TestNegative(self, exp: Expression, word: str):    
        if exp.consume(word) is not None:           
            raise Exception("Consume negative error")            

    def MakeTest(self, exp: Expression, caseNo: int):
        threading.stack_size(227680000)
        sys.setrecursionlimit(2147483647)
        test = Test()
        test.StartTest(caseNo, 1, 100, 'PEG', lambda w: self.TestPositive(exp, w), lambda w: self.TestNegative(exp, w))
        test.StartTest(caseNo, 101, 1000, 'PEG', lambda w: self.TestPositive(exp, w), lambda w: self.TestNegative(exp, w))
        test.StartTest(caseNo, 1001, 10000, 'PEG', lambda w: self.TestPositive(exp, w), lambda w: self.TestNegative(exp, w))
        test.StartTest(caseNo, 10001, 100000, 'PEG', lambda w: self.TestPositive(exp, w), lambda w: self.TestNegative(exp, w))        

threading.stack_size(227680000)
sys.setrecursionlimit(2147483647)

t = threading.Thread(target=ThreadTest())
t.start()
t.join()

print('Test done')
