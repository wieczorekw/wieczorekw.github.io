import random as rand
import os

def Load(fileName: str):    
    data = []
    i = 0
    with open(fileName, 'r') as file:
        fileName = ''
        for line in file:     
            if i % 2 == 1:
                data.append({ 'fileName': fileName, 'word': line.strip() })
            else:
                fileName = line.strip()
            i += 1
    return data

for x in Load('tomita_parsing_errors.txt'):
    with open(x['fileName'], 'w+') as file:
        word = x['word']
        content = file.read()
        content.replace('\n'+word+'\n', '\n'+word + 'bb\n')
        file.write(content)

os.remove('tomita_parsing_errors.txt')

print('Done')
        