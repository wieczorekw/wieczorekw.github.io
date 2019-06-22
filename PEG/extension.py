from anytree import Node, RenderTree, DoubleStyle
from peg import Expression, Terminal, Node as pegNode
from typing import List
from random import randint

def next(expr: Expression) -> List[Expression]:

    if isinstance(expr, Terminal):
        return []    

    if expr.symbol in ("~", "+"):
        yield expr.tree.arg.exp
    
    if hasattr(expr.tree, "left") and expr.tree.left is not None:
        yield expr.tree.left.exp
      
    if hasattr(expr.tree, "right") and expr.tree.right is not None:
        yield expr.tree.right.exp

def all(expr: Expression) -> List[Expression]:
    allExpr = []
    def trav(expr: Expression):
        allExpr.append(expr)
        for exp in next(expr):            
            trav(exp)
        
    trav(expr)
    return allExpr

def printExpression(expr: Expression):

    def to_any_tree(expr: Expression, parent: Node = None):
        node = Node(expr.symbol, parent=parent)        

        for exp in next(expr): 
            to_any_tree(exp, node)        

    root = Node("e")
    
    to_any_tree(expr, root)

    root = root.children[0]

    for pre, _, node in RenderTree(root, style=DoubleStyle):
        print("%s%s" % (pre, node.name))

def switch(first: Expression, firstParent: Expression, second: Expression, secondParent: Expression):
    assert not isinstance(firstParent, Terminal), 'First parent exp to switch cannot be terminal'
    assert not isinstance(secondParent, Terminal), 'Second parent exp to switch cannot be terminal'

    def switchNodes(exp: Expression, expPar: Expression, newNode: pegNode):

        if expPar.symbol in ('+', '~') and id(expPar.tree.arg.exp) == id(exp):
            expPar.tree.arg = newNode
        elif id(expPar.tree.left.exp) == id(exp):            
            expPar.tree.left = newNode
        elif id(expPar.tree.right.exp) == id(exp):            
            expPar.tree.right = newNode
        else:
            raise Exception()    

    def getNode(exp: Expression, expPar: Expression) -> pegNode:
        if expPar.symbol in ('+', '~') and id(expPar.tree.arg.exp) == id(exp):
            return expPar.tree.arg            
        elif id(expPar.tree.left.exp) == id(exp):
            return expPar.tree.left
        elif id(expPar.tree.right.exp) == id(exp):
          return expPar.tree.right
        else:
            raise Exception()

    forFirstNode = getNode(second, secondParent)
    forSecondNode = getNode(first, firstParent)

    switchNodes(first, firstParent, forFirstNode)
    switchNodes(second, secondParent, forSecondNode)    

def height(expr: Expression, currentHeight: int = 0) -> int:
    maxHeight: int = currentHeight
    for exp in next(expr):
        maxHeight = max(maxHeight, height(exp, currentHeight + 1))
    return maxHeight

def count(expr: Expression):
    cnt = 1  
    for exp in next(expr):        
        cnt += count(exp)
    
    return cnt

def heightUp(rootExpr: Expression, expr: Expression, parExpr: Expression) -> int:
    assert id(rootExpr) != id(expr), 'Root and expression cannot be the same instance'
    def countUpInt(currExpr: Expression, currExprPar: Expression, depth: int):
        nonlocal expr
        if id(currExpr) == id(expr) and id(currExprPar) == id(parExpr):
            return depth                
        for exp in next(currExpr):            
            ret = countUpInt(exp, currExpr, depth+1)
            if ret > -1:
                return ret
            
            continue

        return -1
    ret = countUpInt(rootExpr, None, 0)
    assert ret >= 0, 'Expr not found in rootExpr'
    return ret

def walkWithParent(expr: Expression, stepsToEnd: int) -> (Expression, Expression):
    def walk(expr: Expression, parentExpr: Expression) -> (Expression, Expression):
        nonlocal steps
        steps -= 1
        if steps == 0:
            return (expr, parentExpr)

        for exp in next(expr):            
            (resExp, resParExpr) = walk(exp, expr)
            if resExp is not None:
                return (resExp, resParExpr)
        return (None, None)
    steps = stepsToEnd

    return walk(expr, None)

def walk(expr: Expression, stepsToEnd: int) -> Expression:
    return walkWithParent(expr, stepsToEnd)[0]

def randomWalk(expr: Expression, min: int) -> (Expression, Expression):
    if expr is None:
        raise Exception()
    steps = randint(min, count(expr))

    return walkWithParent(expr, steps)

def randomSwitch(first: Expression, second: Expression, min: int = 2, maxDepth: int = 0, retryCount: int = 30):
    assert min > 1, 'The minimum of step must be more than 1'
    assert height(first) < maxDepth or maxDepth == 0, 'First expression exceed max depth'
    assert height(second) < maxDepth or maxDepth == 0, 'Second expression exceed max depth'

    while(True):
        if retryCount <= 0:
            return

        (rndFirst, rndFirstParent) = randomWalk(first, min)
        (rdnSecond, rdnSecondParent)= randomWalk(second, min)

        if maxDepth > 0 and heightUp(first, rndFirst, rndFirstParent) + height(rdnSecond) + 1 > maxDepth:
            retryCount-=1
            continue
        elif maxDepth > 0 and heightUp(second, rdnSecond, rdnSecondParent) + height(rndFirst) + 1 > maxDepth:
            retryCount-=1
            continue
        else:
            break

    assert rndFirst is not None, 'Random exp cannot be None'
    assert rdnSecond is not None, 'Random exp cannot be None'
    assert rndFirstParent is not None, 'Random parent exp cannot be None'
    assert rdnSecondParent is not None, 'Random parent exp cannot be None'

    switch(rndFirst, rndFirstParent, rdnSecond, rdnSecondParent)

    assert height(first) < maxDepth or maxDepth == 0, 'Switched first expression exceed max depth'
    assert height(second) < maxDepth or maxDepth == 0, 'Switched second expression exceed max depth'