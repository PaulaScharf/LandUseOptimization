# LandUseOptimization
Land Use Optimization towards mining with minimal ecological impact in Mato Grosso, Brazil

# Results
![image of pareto front](/figures/pareto_front_over_generations_3d.png)

The pareto front, displayed by generations.
![image of example best fit](/figures/best_yield_study2.png)

An optimized solution for mining yield.

# Objectives
## maximize mining

#### parameters
	a1 = prize of gold per kg, a2 = avarage gold yield in kg per km2
	b1 = prize of sandstone per kg, a2 = avarage sandstone yield in kg per km2
	...
      
#### variables
	x = area for goldmining in km2
	y = area for sandstone mining in km2
	...
#### function
	f(x,y,...) = x*a1*a2 + y*b1*b2 + ... = total revenue


## minimize loss of biomass
#### parameters
	a = biomass for forrest per km2
	b = biomass for pasture per km2
	...
#### variables
	x = area of forrest in km2
	y = area of pasture in km2
	...
#### function
	f(x,y,...) = x*a + y*b + ... = total biomass
