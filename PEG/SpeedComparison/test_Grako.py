from peg_common import *
from grako import compile,parse
import threading

class GrakoParseException(Exception):
    pass

class ThreadTest:
    def __call__(self):
        self.MakeTest(self.Case1(), 1)
        self.MakeTest(self.Case2(), 2)
        #self.MakeTest(self.Case3(), 3)
        self.MakeTest(self.Case4(), 4)
        self.MakeTest(self.Case5(), 5)
        self.MakeTest(self.Case6(), 6)
        self.MakeTest(self.Case7(), 7)

    def Case1(self):
		#Test Case 1    
        return '''
            start = S $ ;     
            a = "a" ;
            b = "b" ;
            S = {a}+ !(a | b);
            '''     
            
    def Case2(self):
		#Test Case 2        
        return '''
            start = S $; 
            a = "a" ; 
            b = "b" ; 
            C = a b ;
            S = {C}+ !(a | b) ;
            '''

    def Case3(self):
		#Test Case 3 
        return 'a <- \'a\'; b <- \'b\'; A <- a !a / a a A;'+\
			r'B <- b !b / b b B;'+\
			r'C <- a A / !a;'+\
			r'D <- b B / !b;'+\
			r'S <- (a a / b)+ S / (A D S) / !(a / b);'    

    def Case4(self):
		#Test Case 4
        return '''
            start = S $; 
            a = "a" ; 
            b = "b" ; 
            D = (b b | b) {a}+ ;
            C = ({D}+ | {}) ;        
            S = ({a}+ | {}) C (b b !(a | b) | b !(a | b) | !(a | b)) ;
            '''            

    def Case5(self):
		#Test Case 5      
        return '''
            start = S $; 
            a = "a" ; 
            b = "b" ;              
			A = {D}+ | {} ;
			B = a b | b a ;
            C = B A B A ; 
            D = a a | b b ;
			S = A ({C}+ | {}) A !(a | b) ;
            '''

    def Case6(self):
		#Test Case 6
        return '''
            start = S $; 
            a = "a" ; 
            b = "b" ; 
            C = a b ;
            D = b a ;   
            E = A | B ;
            A = a ({C}+ | {})(b | a a) ;
			B = b ({D}+ | {})(a | b b) ;
			S = {E}+ !(a | b) | !(a | b) ;
            '''

    def Case7(self):
		#Test Case 7
        return '''
            start = S $; 
            a = "a" ;
            b = "b" ;
			A = {a}+ | {} ;
			B = {b}+ | {} ;
			S = A B A B !(a | b) ;    
            '''

    def TestPositive(self, model, word: str):
        try:            
            model.parse(word)
        except Exception as e:
            raise e

    def TestNegative(self, model, word: str):
        try:                    
            model.parse(word)
            raise GrakoParseException("Parse negative error")
        except GrakoParseException as ex:
            raise ex
        except Exception:            
            pass

    def MakeTest(self, exp, caseNo: int):    
        test = Test()                  
        model = compile(exp)        
        test.StartTest(caseNo, 1, 100, 'Grako', lambda w: self.TestPositive(model, ' '.join(w)), lambda w: self.TestNegative(model, ' '.join(w)))
        test.StartTest(caseNo, 101, 1000, 'Grako', lambda w: self.TestPositive(model, ' '.join(w)), lambda w: self.TestNegative(model, ' '.join(w)))
        test.StartTest(caseNo, 1001, 10000, 'Grako', lambda w: self.TestPositive(model, ' '.join(w)), lambda w: self.TestNegative(model, ' '.join(w)))
        test.StartTest(caseNo, 10001, 100000, 'Grako', lambda w: self.TestPositive(model, ' '.join(w)), lambda w: self.TestNegative(model, ' '.join(w)))        

t = threading.Thread(target=ThreadTest())
t.start()
t.join()
print('Test done')
