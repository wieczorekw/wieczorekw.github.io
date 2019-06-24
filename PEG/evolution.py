from induce import induce
from peg import Expression
from extension import randomSwitch, count, height
from typing import List, Callable
from random import sample, random, randrange
from copy import deepcopy, copy
from statistics import mean, median

class Individual:

    expression: Expression
    fitness: float

    def __init__(self, expression: Expression, fitness: float):
        self.expression = expression
        self.fitness = fitness        
    
    @classmethod
    def random(cls, X: set, Y: set, sampleSize, depthSize: int, fitness: Callable[[Expression], float]):        
        tryCount: int = 0
        while(tryCount < 30):
            exp = induce(sample(X, sampleSize), sample(Y, sampleSize))

            if height(exp) > depthSize:
                continue

            fit: float = fitness(exp)
            return cls(exp, fit)
            
        raise NameError("Try 30 times to create expression with depth less then {0}".format(depthSize))

    def __str__(self):
        return "fitness: {0:.4f}, size: {1}".format(self.fitness, len(self.expression.__str__()))

class Evolution:
    population: List[Individual]
    nextPopulation: List[Individual]
    populationSize: int
    sampleSize: int
    X: set
    Y: set
    WordSetSize: float
    maxDepth: int
    crossOverRate: float
    tournamentSize: int    

    def __init__(self, populationSize: int, sampleSize: int, maxDepth: int, crossOverRate: float, tournamentSize: int, X: set, Y: set):
        """Init algorithm
        Keyword arguments:
        populationSize -- population size
        sampleSize -- number of sampling used to induce when create individual
        maxDepth -- maximal depth of the graph
        crossOverRate -- probability of cross over
        tournamentSize -- the size of list using by selection function, the best individual from that list will be parent
        X -- example set
        Y -- co-example set
        """
        self.populationSize = populationSize
        self.sampleSize = sampleSize
        self.X = X
        self.Y = Y
        self.maxDepth = maxDepth
        self.crossOverRate = crossOverRate
        self.WordSetSize = len(X) + len(Y)
        self.tournamentSize = tournamentSize        

    def initPopulation(self):
        self.population = [None] * self.populationSize

        for i in range(self.populationSize):  
            self.population[i] = Individual.random(self.X, self.Y, self.sampleSize, self.maxDepth, self.fitness)            

    def initNextPopulation(self):
        self.nextPopulation = [None] * self.populationSize
        
    def fitness(self, ind: Expression) -> float:
        counter: float = 0.0
        for word in self.X:
            counter += 1.0 if ind.consume(word) else 0.0
        
        for word in self.Y:
            counter += 1.0 if ind.consume(word) is None else 0.0

        return counter / self.WordSetSize

    def crossOver(self, first: Individual, second: Individual) -> [Individual]:
        if random() <= self.crossOverRate:
            firstCopy = deepcopy(first.expression)
            secondCopy = deepcopy(second.expression)            

            randomSwitch(firstCopy, secondCopy, maxDepth=self.maxDepth)

            firstChild = Individual(firstCopy, self.fitness(firstCopy))
            secondChild = Individual(secondCopy, self.fitness(secondCopy))

            return [firstChild, secondChild]
        
        return [first, second]

    def selection(self) -> Individual:
        maxIdx =  randrange(0, self.populationSize)    

        for _ in range(1, self.tournamentSize):
            candIdx = randrange(0, self.populationSize)
            if self.population[candIdx].fitness > self.population[maxIdx].fitness:
                maxIdx = candIdx

        return self.population[maxIdx]

    def succession(self, first: Individual, second: Individual):
        return first if first.fitness > second.fitness else second
        
    def dump(self):
        [print(ind) for ind in self.population]

    def bestIndividual(self, iterable: List[Individual]):
        return max(iterable, key=lambda ind: ind.fitness)

    def evolving(self, interations: int, debugOn: bool = False, statOn: bool = False) -> Individual:
        """Main optimization function."""
        self.initPopulation()

        if debugOn:
            self.dump()

        self.initNextPopulation()         

        best: Individual = self.bestIndividual(self.population)

        for i in range(interations):
            self.nextPopulation[0] = best

            for k in range(1, self.populationSize):
                child1, child2 = self.crossOver(self.selection(), self.selection())                
                self.nextPopulation[k] = self.succession(child1, child2)                
            
            self.population = copy(self.nextPopulation)            

            if debugOn:
                self.dump()

            if statOn:
                fitnesses = list(map(lambda ind: ind.fitness, self.population))
                print("fitness at {0}: min={1:.4f}; median={2:.4f}; max={3:.4f}".format(i, min(fitnesses), median(fitnesses), max(fitnesses)))

                treeHeights = list(map(lambda ind: height(ind.expression), self.population))
                print("exp. heights at {0}: min={1:.4f}; median={2:.4f}; max={3:.4f}".format(i, min(treeHeights), median(treeHeights), max(treeHeights)))

                treeNodeCounts = list(map(lambda ind: count(ind.expression), self.population))
                print("exp. node count at {0}: min={1:.4f}; median={2:.4f}; max={3:.4f}".format(i, min(treeNodeCounts), median(treeNodeCounts), max(treeNodeCounts)))

                divers = set()
                [divers.add(ind.expression) for ind in self.population]
                print("exp. unique at {0}: {1}/{2}".format(i, len(divers), self.populationSize))

            itbest = self.bestIndividual(self.population)

            if itbest.fitness > best.fitness:
                best = deepcopy(itbest)

        return best


