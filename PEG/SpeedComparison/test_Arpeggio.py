from peg_common import *
from arpeggio.peg import ParserPEG
from arpeggio import *

import threading
import sys

class ThreadTest:
    def __call__(self):
        self.MakeTest(ParserPEG(self.Case1(), "S"), 1)
        self.MakeTest(ParserPEG(self.Case2(), "S"), 2)
        #self.MakeTest(ParserPEG(self.Case3(), "S"), 3)
        self.MakeTest(ParserPEG(self.Case4(), "S"), 4)
        self.MakeTest(ParserPEG(self.Case5(), "S"), 5)
        self.MakeTest(ParserPEG(self.Case6(), "S"), 6)
        self.MakeTest(ParserPEG(self.Case7(), "S"), 7)
    def Case1(self):
		#Test Case 1    
        return 'a <- \'a\'; b <- \'b\'; S <- a+ !(a / b);'

    def Case2(self):
		#Test Case 2
        return 'a <- \'a\'; b <- \'b\'; S <- (a b)+ !(a / b);'

    def Case3(self):
		#Test Case 3 
        return 'a <- \'a\'; b <- \'b\'; A <- a !a / a a A;'+\
			r'B <- b !b / b b B;'+\
			r'C <- a A / !a;'+\
			r'D <- b B / !b;'+\
			r'S <- (a a / b)+ S / (A D S) / !(a / b);'    

    def Case4(self):
		#Test Case 4
        #return 'a <- \'a\'; b <- \'b\';' +\
        #    'C <- (b b / b) a a*;' +\
        #    'S <- a* C* b b / b / a*;' 
        return 'a <- \'a\'; b <- \'b\';' +\
            'S <- a* (b b a / b a / a)* (b b / b)? EOF;'

    def Case5(self):
		#Test Case 5    
        return 'a <- \'a\'; b <- \'b\'; epsilon <- \'\';'+\
			r'A <- (a a / b b)+ / epsilon;' +\
			r'B <- a b / b a;' +\
			r'S <- A ((B A B A)+ / epsilon) A !(a / b);'    

    def Case6(self):
		#Test Case 6
        return 'a <- \'a\'; b <- \'b\'; epsilon <- \'\'; A <- a ((a b)+ / epsilon)(b / a a);'+\
			r'B <- b ((b a)+ / epsilon)(a / b b);'+\
			r'S <- (A / B)+ !(a / b) / !(a / b);' 

    def Case7(self):
		#Test Case 7
        return 'a <- \'a\'; b <- \'b\'; epsilon <- \'\';'+\
			r'A <- a+ / epsilon;'+\
			r'B <- b+ / epsilon;'+\
			r'S <- A B A B !(a / b);'    

    def TestPositive(self, parser, word: str):
        try:        
            parser.parse(word)
        except NoMatch as e:
            raise e
        except Exception as e:
            raise e

    def TestNegative(self, parser, word: str):
        try:        
            parser.parse(word)
            raise Exception("Parse negative error")
        except NoMatch:
            pass

    def MakeTest(self, parser, caseNo: int):    
        test = Test()
        test.StartTest(caseNo, 1, 100, 'Arpeggio', lambda w: self.TestPositive(parser, w), lambda w: self.TestNegative(parser, w))
        test.StartTest(caseNo, 101, 1000, 'Arpeggio', lambda w: self.TestPositive(parser, w), lambda w: self.TestNegative(parser, w))
        test.StartTest(caseNo, 1001, 10000, 'Arpeggio', lambda w: self.TestPositive(parser, w), lambda w: self.TestNegative(parser, w))
        test.StartTest(caseNo, 10001, 100000, 'Arpeggio', lambda w: self.TestPositive(parser, w), lambda w: self.TestNegative(parser, w))        

t = threading.Thread(target=ThreadTest())
t.start()
t.join()
print('Test done')