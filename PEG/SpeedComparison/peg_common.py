import time
import random as rand
import re
import sys
sys.path.insert(0, '\\rstr')
import rstr
from peg import *

class Test:
    def StartTest(self, case: int, minCount: int, maxCount: int, alg: str, makePositiveTest, makeNegativeTest, repeats: int = 30):        
        with open('tomita_Case{0}_result.txt'.format(case), 'a') as resultFile,\
             open('tomita_parsing_errors.txt', 'a') as errorFile:
                fileName = self.__CreateName('positive', case, minCount, maxCount)
                positive = self.__Load(fileName)
                avg_time = 0
                for rep in range(repeats):
                    start = time.time()        
                    for w in positive:
                        try:
                            makePositiveTest(w)           
                        except Exception as e:
                            errorFile.write('{0}\n{1}\n'.format(fileName, w))
                            print('Error')
                    end = time.time()
                    avg_time += end - start
                resultFile.write('{3};positive;{0}-{1};{2:.2f}\n'.format(minCount, maxCount, avg_time / repeats, alg))
                fileName = self.__CreateName('negative', case, minCount, maxCount)
                negative = self.__Load(fileName)
                avg_time = 0
                for rep in range(repeats):
                    start = time.time()        
                    for w in negative:
                        try:
                            makeNegativeTest(w)
                        except Exception as e:
                            errorFile.write('{0}\n{1}\n'.format(fileName, w))
                            print('Error')
                    end = time.time()
                    avg_time += end - start
                resultFile.write('{3};negative;{0}-{1};{2:.2f}\n'.format(minCount, maxCount, avg_time / repeats, alg))

    def CreateTestCase(self, caseId: int, count: int, wordSizeMin: int, wordSizeMax: int, reg: str):
        try:        
            w = ''  
            print("Generating {0} {1}-{2}".format(caseId, wordSizeMin, wordSizeMax))
            with open(self.__CreateName('positive', caseId, wordSizeMin, wordSizeMax), 'w') as file1,\
                 open(self.__CreateName('negative', caseId, wordSizeMin, wordSizeMax), 'w') as file2:                
                    unique = []
                    for i in range(count):
                        print("Word: {0}".format(i+1))
                        tooLow,tooHigh = 0,0
                        currWordSizeMin, currWordSizeMax = wordSizeMin, wordSizeMax
                        regGen, currWordSizeMin, currWordSizeMax = self.__CalculateRepetitions(reg, currWordSizeMin, currWordSizeMax, tooLow, tooHigh)            
                        while True:                        
                            if tooLow > 3 or tooHigh > 3:
                                regGen, currWordSizeMin, currWordSizeMax = self.__CalculateRepetitions(reg, currWordSizeMin, currWordSizeMax, tooLow, tooHigh)
                                tooLow = tooHigh = 0
                            pattern = re.compile(reg)
                            #positive                        
                            w = rstr.xeger(regGen)
                            if len(w) < wordSizeMin:
                                tooLow += 1
                                continue
                            elif len(w) > wordSizeMax:
                                tooHigh += 1
                                continue
                            if w in unique:
                                continue
                            if pattern.fullmatch(w) is None:
                                continue
                            unique.append(w)
                            file1.write(w+'\n')                        
                            #negative
                            if len(w) == 0:
                                w = str(rand.choice(['a','b']))
                                print("Zero length")
                            counter = 0                            
                            try:
                                while True:
                                    counter += 1                                
                                    list1 = list(w)
                                    pos = rand.randint(0, len(w)-1)
                                    list1[pos] = rand.choice(['a','b'])
                                    w = ''.join(list1)
                                    if counter > 3:
                                        w += str(rand.choice(['a','b']))
                                    if pattern.fullmatch(w) is None:
                                        file2.write(w+'\n')                                    
                                        break
                                break
                            except Exception as e:
                                print("Error while parsing: {0}".format(e))
                                with open(__CreateName('error', caseId, wordSizeMin, wordSizeMax), 'w') as fileE:
                                    fileE.write(w+'\n')
                            break                    
        except Exception as e:
            print("General error parsing: {0}".format(e))
            with open(self.__CreateName('error', caseId, wordSizeMin, wordSizeMax), 'w') as fileE:
                fileE.write(w+'\n')   

    def __CreateName(selft, type: str, caseId: int, wordSizeMin: int, wordSizeMax: int):
        wordSizeMinStr = str(wordSizeMin//1000) + 'k' if wordSizeMin >= 1000 else wordSizeMin
        wordSizeMaxStr = str(wordSizeMax//1000) + 'k' if wordSizeMax >= 1000 else wordSizeMax
        return '{0}_Case{1}_{2}-{3}_{4}.txt'.format('tomita', caseId, wordSizeMinStr, wordSizeMaxStr, type)

    def __Load(self, fileName: str):    
        words = []
        with open(fileName, 'r') as file:
            for line in file:            
                words.append(line.strip())
        return words

    def __CalculateRepetitions(self, reg: str, wordSizeMin: int, wordSizeMax: int, tooLow: int, tooHigh: int):
        if tooLow > tooHigh:
            wordSizeMin *= 2 if wordSizeMax < 1000 else 10
            wordSizeMax *= 2 if wordSizeMax < 1000 else 10
        elif tooLow < tooHigh:        
            wordSizeMin //= 2 if wordSizeMax < 1000 else 10
            wordSizeMax //= 2 if wordSizeMax < 1000 else 10
            wordSizeMax = max(1, wordSizeMax)
        else:
            starPlusCount = reg.count('+') + reg.count('*')
            wordSizeMin //= starPlusCount
            wordSizeMax //= starPlusCount
            wordSizeMin = min(max(0, wordSizeMin), 100)
            wordSizeMax = min(max(1, wordSizeMax), 1000)        

        regGen = reg.replace(r'+', r'{{{0},{1}}}'.format(max(1, wordSizeMin), wordSizeMax))
        regGen = regGen.replace(r'*', r'{{{0},{1}}}'.format(wordSizeMin, wordSizeMax))
        print('Regex: {0}'.format(regGen))
        return regGen, wordSizeMin, wordSizeMax


