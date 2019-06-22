from extension import printExpression, switch, all, height, count, walk, randomWalk, randomSwitch, walkWithParent,heightUp
from peg import Expression, Terminal
from induce import induce
from random import choices, randint
from copy import deepcopy

def TestHeight1():
    A : Expression = induce(['aba','abb','abc'],['aa','ab','ac','abcd'])     
    h = height(A)   
    assert(h in (5, 6))

def TestHeight2():
    a = Terminal('a')
    b = Terminal('b')
    B = Expression('B')
    B = a | ~b >> a | ~b    
    assert(height(B) == 4)

def TestHeight3():
    a = Terminal('a')
    B = Expression('B')
    B = a >> a    
    assert(height(B) == 1)

def TestCount():
    A : Expression = induce(['aba','abb','abc'],['aa','ab','ac','abcd'])    
    assert(count(A) == 12)

    a = Terminal('a')
    B = Expression('B')
    B = a >> a    
    assert(count(B) == 3)
    
def TestWalk():
    A : Expression = induce(['aba','abb','abc'],['aa','ab','ac','abcd'])
    
    # print("all:")
    # [print(a.symbol) for a in all(A)]
    # print("walk:")
    # [print(walkWithParent(A, i)[0].symbol) for i in range(1, 13)]
    # print("end")
    assert(walk(A, 1).symbol == all(A)[0].symbol)
    assert(walk(A, 2).symbol == all(A)[1].symbol)
    assert(walk(A, 3).symbol == all(A)[2].symbol)
    assert(walk(A, 4).symbol == all(A)[3].symbol)
    assert(walk(A, 5).symbol == all(A)[4].symbol)
    assert(walk(A, 6).symbol == all(A)[5].symbol) 
    assert(walk(A, 7).symbol == all(A)[6].symbol)
    assert(walk(A, 8).symbol == all(A)[7].symbol)
    assert(walk(A, 9).symbol == all(A)[8].symbol) 
    assert(walk(A, 10).symbol == all(A)[9].symbol)
    assert(walk(A, 11).symbol == all(A)[10].symbol)
    assert(walk(A, 12).symbol == all(A)[11].symbol) 
    assert(walk(A, 13) is None)
    assert(walk(A, 14) is None)

def SimpleWalkTest():
    a = Terminal('a')
    b = Terminal('b')
    A = Expression('A')
    A = a | ~b >> a | ~b            
    assert(walkWithParent(A, 1)[1] == None)
    assert(walkWithParent(A, 1)[0].symbol == '|')
    assert(walkWithParent(A, 2)[1].symbol == '|')
    assert(walkWithParent(A, 2)[0].symbol == '|')
    assert(walkWithParent(A, 3)[1].symbol == '|')
    assert(walkWithParent(A, 3)[0].symbol == 'a')
    assert(walkWithParent(A, 4)[1].symbol == '|')
    assert(walkWithParent(A, 4)[0].symbol == '>>')
    assert(walkWithParent(A, 5)[1].symbol == '>>')
    assert(walkWithParent(A, 5)[0].symbol == '~')
    assert(walkWithParent(A, 6)[1].symbol == '~')
    assert(walkWithParent(A, 6)[0].symbol == 'b')
    assert(walkWithParent(A, 7)[1].symbol == '>>')
    assert(walkWithParent(A, 7)[0].symbol == 'a')
    assert(walkWithParent(A, 8)[1].symbol == '|')
    assert(walkWithParent(A, 8)[0].symbol == '~')
    assert(walkWithParent(A, 9)[1].symbol == '~')
    assert(walkWithParent(A, 9)[0].symbol == 'b')
    assert(walkWithParent(A, 10)[0] == None)
    assert(walkWithParent(A, 10)[1] == None)

def RandomWalk():
    a = Terminal('a')
    b = Terminal('b')
    B = Expression('B')
    B = a >> ~b
    hit = set()
    uniqueExpr = set()
    for _ in range(1000):
        (ret,_) = randomWalk(B, 1)
        assert(ret is not None)
        hit.add(hex(id(ret)))
        uniqueExpr.add(ret.__str__())
    assert(len(hit) == 4)    
    assert(len(uniqueExpr) == 4)
    A : Expression = induce(['aba','abb','abc'],['aa','ab','ac','abcd'])
    hit.clear()
    uniqueExpr.clear()
    for _ in range(1000):
        (ret,_) = randomWalk(A, 1)
        assert(ret is not None)
        hit.add(hex(id(ret)))
        uniqueExpr.add(ret.__str__())

    assert(len(hit) == 10)
    assert(len(uniqueExpr) == 10)

def TestSwitch():
    X = ['aba','abb','abc']
    Y = ['aa','ab','ac','abcd']
    for _ in range(1000):
        A : Expression = induce(X, Y)
        B : Expression = induce(X, Y)

        randomSwitch(A, B, 2)

        for word in zip(X, Y):
            A.consume(word)        

def TestBasicSwitch():
    X = ['aba','abb','abc']
    Y = ['aa','ab','ac','abcd']
    
    A: Expression
    B: Expression
    A2: Expression
    B2: Expression
    for _ in range(1000):        
        a = Terminal('a')
        b = Terminal('b')
        A = Expression('A')
        A = a >> b >> ~b >> a
        B = Expression('B')
        B = b >> a >> a >> b                       

        (A2, A2Par) = randomWalk(A, 2)
        (B2, B2Par) = randomWalk(B, 2)

        switch(A2, A2Par, B2, B2Par)

        for word in zip(X, Y):
            A.consume(word) 
            B.consume(word)
    
def RandomNew(alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','w','x','y','z']):
    X = []
    Y = []    
    for _ in range(30):
        X.append("".join(choices(alphabet, k=randint(3, 15))))

    for _ in range(30):
        word = "".join(choices(alphabet, k=randint(3, 15)))
        if word not in X:
            Y.append(word)
    return X, Y

def TestTheSameSwitch():
    for _ in range(100):
        X, Y = RandomNew()
        A = induce(X, Y)    
        B = induce(X, Y)

        rand = randint(2, count(A))

        (A2, A2Par) = walkWithParent(A, rand)
        (B2, B2Par) = walkWithParent(B, rand)

        switch(A2, A2Par, B2, B2Par)

        for word in X:
            if not A.consume(word):
                raise AssertionError

            if not B.consume(word):
                raise AssertionError

        for word in Y:
            if A.consume(word):
                raise AssertionError

            if B.consume(word):
                raise AssertionError

def TestSwitchConsistency1():
    #non terminal

    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    A = Expression('A')
    B = Expression('B')
    A = a >> ~a | c
    B = a | b >> b

    (nodeA, parA) = walkWithParent(A, 2)
    (nodeB, parB) = walkWithParent(B, 3)

    switch(nodeA, parA, nodeB, parB)

    assert(A.__str__() == 'b >> b | c')
    assert(B.__str__() == 'a | a >> ~a')

def TestSwitchConsistency2():
    #terminal

    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    A = Expression('A')
    B = Expression('B')
    A = a >> ~a | c
    B = a | b >> b

    (nodeA, parA) = walkWithParent(A, 3)
    (nodeB, parB) = walkWithParent(B, 3)

    switch(nodeA, parA, nodeB, parB)

    assert(A.__str__() == 'b >> b >> ~a | c')
    assert(B.__str__() == 'a | a')

def TestSwitchConsistency3():
    #unary

    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    A = Expression('A')
    B = Expression('B')
    A = a >> ~a | c
    B = a | b >> b

    (nodeA, parA) = walkWithParent(A, 4)
    (nodeB, parB) = walkWithParent(B, 3)

    switch(nodeA, parA, nodeB, parB)

    assert(A.__str__() == 'a >> b >> b | c')
    assert(B.__str__() == 'a | ~a')

def TestSwitchConsistency4():
    #unary 2

    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    A = Expression('A')
    B = Expression('B')
    A = a >> ~a | c
    B = a | b >> b

    (nodeA, parA) = walkWithParent(A, 5)
    (nodeB, parB) = walkWithParent(B, 3)

    switch(nodeA, parA, nodeB, parB)

    assert(A.__str__() == 'a >> ~(b >> b) | c')
    assert(B.__str__() == 'a | a')

def TestRandomSwitchConsistency():
    for _ in range(100):
        alphabet = ['a','b','c','d','e','f','g','h','i','j','k']
        X, Y = RandomNew(alphabet)
        A: Expression = induce(X, Y)
        alphabet = ['l','m','n','o','p','r','s','t','u','w','x','y','z']
        X, Y = RandomNew(alphabet)
        B: Expression = induce(X, Y)

        expABefore: str = A.__str__()
        expBBefore: str = B.__str__()

        cpyA = deepcopy(A)
        cpyB = deepcopy(B)

        expCpyABefore = cpyA.__str__()
        expCpyBBefore = cpyB.__str__()

        randomSwitch(cpyA, cpyB)        

        expAAfter: str = A.__str__()
        expBAfter: str = B.__str__()

        assert(expABefore == expAAfter)
        assert(expBBefore == expBAfter)        

        expCpyAAfter: str = cpyA.__str__()
        expCpyBAfter: str = cpyB.__str__()

        assert(expAAfter != expCpyAAfter)
        assert(expBAfter != expCpyBAfter)

        assert(expCpyABefore != expCpyAAfter)
        assert(expCpyBBefore != expCpyBAfter)

        unique = set([expABefore, expBBefore, expAAfter, expBAfter, expCpyABefore, expCpyBBefore, expCpyAAfter, expCpyBAfter])

        assert(len(unique) == 4)

def TestHeightUp():
    a = Terminal('a')
    b = Terminal('b')
    c = Terminal('c')
    d = Terminal('d')
    A = Expression('A')
    A = a >> b >> (b | a | c >> ~d)    

    (exp, parExp) = walkWithParent(A, 8)        
    assert(heightUp(A, exp, parExp) == 3)

    (exp, parExp) = walkWithParent(A, 12)    
    assert(heightUp(A, exp, parExp) == 4)

    (exp, parExp) = walkWithParent(A, 4)    
    assert(heightUp(A, exp, parExp) == 2)

    (exp, parExp) = walkWithParent(A, 2)
    assert(heightUp(A, exp, parExp) == 1)

def TestHeightHeightUp():
    for _ in range(100):
        X = []
        Y = []

        alphabet = ['a','b','c','d','e','f','g','h','i','j','k']
        X, Y = RandomNew(alphabet)
        A = induce(X, Y)

        alphabet = ['l','m','n','o','p','r','s','t','u','w','x','y','z']
        X, Y = RandomNew(alphabet)
        B = induce(X, Y)

        AExp = A.__str__()
        BExp = B.__str__()

        (first, firstPar) = randomWalk(A, 2)    
        (second, secondPar) = randomWalk(B, 2)

        theoreticalHeightA = heightUp(A, first, firstPar) + height(second)
        theoreticalHeightB = heightUp(B, second, secondPar) + height(first)

        switch(first, firstPar, second, secondPar)

        sizeAAfter = heightUp(A, second, firstPar) + height(second)
        sizeBAfter = heightUp(B, first, secondPar) + height(first)

        assert(theoreticalHeightA == sizeAAfter)
        assert(theoreticalHeightB == sizeBAfter)
        assert(AExp != A.__str__())
        assert(BExp != B.__str__())

TestHeight1()
TestHeight2()
TestHeight3()
TestCount()
TestWalk()
SimpleWalkTest()
RandomWalk()
TestSwitch()
TestBasicSwitch()
TestTheSameSwitch()
TestSwitchConsistency1()
TestSwitchConsistency2()
TestSwitchConsistency3()
TestSwitchConsistency4()
TestRandomSwitchConsistency()
TestHeightUp()
TestHeightHeightUp()