import numpy as np
parent1 = np.array([
[True,'gold',500,300],
[False,'diamonds',400,600],
[True,'gold',300,100],
[True,'diamonds', 200,800],
[False,'gold', 100,300]])
parent2 = np.array([
[False,'gold',500,300],
[False,'diamonds',400,600],
[True,'gold',300,100],
[True,'diamonds',200,800],
[True,'gold',100,300]])
population = [parent1, parent2]
print(population[0][:,0])
