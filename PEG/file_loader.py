def readFileLines(file, list):
    for line in file:
        if line == '\n':
            break
        list.append(line.strip())    

def loadData(fileName, X, Y):
    X = [] if X is None else X
    Y = [] if Y is None else Y
    with open(fileName, 'r') as file:
        readFileLines(file, X)
        readFileLines(file, Y)