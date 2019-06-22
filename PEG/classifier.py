from evolution import Evolution
from file_loader import loadData

X = []
Y = []
loadData('randomdata_4_500_500_3_30.txt', X, Y)

evolutionAlgorithm = Evolution(20, 20, 20, 0.9, 3, X, Y)
wyr = evolutionAlgorithm.evolving(40, False, True)
