from peg_common import *


def CreateTest(caseId: int, reg: str):    
    test = Test()
    test.CreateTestCase(caseId, 30, 1, 100, reg)    
    test.CreateTestCase(caseId, 30, 101, 1000, reg)    
    test.CreateTestCase(caseId, 30, 1001, 10000, reg)    
    test.CreateTestCase(caseId, 30, 10001, 100000, reg)    
    test.CreateTestCase(caseId, 30, 100001, 1000000, reg)

CreateTest(1, r'a+')
CreateTest(2, r'(ab)*')
CreateTest(3, r'((b|(aa))|(((a(bb))((bb)|(a(bb)))*)(aa)))*((a+)|(((a(bb))((bb)|(a(bb)))*)(a+)))')
CreateTest(4, r'a*((b|bb)aa*)*(b|bb|a*)')
CreateTest(5, r'(aa|bb)*((ba|ab)(bb|aa)*(ba|ab)(bb|aa)*)*(aa|bb)*')
CreateTest(6, r'((a(ab)*(b|aa))|(b(ba)*(a|bb)))*')    
CreateTest(7, r'a*b*a*b*')
print("Done")