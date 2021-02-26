# Allocation of Mining Sites to Optimize Land Use
Land Use Optimization towards mining with minimal ecological impact in Mato Grosso, Brazil

---

# How to run the optimization
1. Install the necessary libraries by running the command `pip install requirements.txt`. It is recommended to install the libraries in a dedicated environment (e.g. using Anaconda).
2. Adjust the desired input adress in the file `init_pop.py` if necessary.
3. Execute the main file by running the command `python run_nsga2_spatial.py`.

# Results
![image of pareto front](/figures/pareto_front_over_generations_3d.png)

The pareto front, displayed by generations.
![image of example best fit](/figures/best_yield_study2.png)

An optimized solution for mining yield.

More visualizations of the results can be found in the folder "[figures](https://github.com/PaulaScharf/LandUseOptimization/tree/main/figures)".

---

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
