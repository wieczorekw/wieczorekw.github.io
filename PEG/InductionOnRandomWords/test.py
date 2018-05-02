from peg import *
from induce import *

def compress(expr):
    return expr.__str__().replace('>>', '').replace(' ', '')

def read_file_lines(file, list):
    for line in file:
        if line == '\n':
            break
        list.append(line.strip())    

def load_data(fileName, X, Y):
    X = [] if X is None else X
    Y = [] if Y is None else Y
    with open(fileName, 'r') as file:
        read_file_lines(file, X)
        read_file_lines(file, Y)
        
def test(fileName):
    str = ''
    str += 'File: {}\n'.format(fileName)
    X = []
    Y = []    
    load_data(fileName, X, Y)
    str += 'PEG length: {}\n'.format(len(compress(induce(X,Y))))
    with open(fileName, 'r') as file:
        str += 'Characters in file: {}\n'.format(sum(len(compress(line)) for line in file))    
    return str + '\n'

with open('result', 'w') as file:
    file.write(test('randomdata_2_10_10_1_10.txt'))
    file.write(test('randomdata_2_100_100_2_20.txt'))
    file.write(test('randomdata_4_500_500_3_30.txt'))
    file.write(test('randomdata_4_1000_1000_4_40.txt'))
    file.write(test('randomdata_8_5000_5000_5_50.txt'))
    file.write(test('randomdata_8_6000_6000_6_60.txt'))
    file.write(test('randomdata_16_7000_7000_7_70.txt'))
    file.write(test('randomdata_16_8000_8000_8_80.txt'))
    file.write(test('randomdata_32_9000_9000_9_90.txt'))
    file.write(test('randomdata_32_10000_10000_10_100.txt'))