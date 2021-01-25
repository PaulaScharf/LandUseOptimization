import numpy as np
# import pickle
import matplotlib.pyplot as plt
# import plotly.graph_objects as go
import plotly.express as px


default_directory = "./"

resX = np.load("./results/resX.npy", allow_pickle=True)
resF = np.load("./results/resF.npy", allow_pickle=True)
# resHist = np.load("./results/resHist.npy", allow_pickle=True)
f = np.load("./results/f.npy", allow_pickle=True)


# Plot of 2D pareto fronts
f1, (ax1a, ax1b, ax1c) = plt.subplots(1, 3, figsize=(15, 5))
ax1a.scatter(-resF[:, 0], -resF[:, 1]) #, s=30, fc='none', ec='k')
ax1a.set_title('objective space / pareto front')
ax1a.set_xlabel('Total yield [€]')
ax1a.set_ylabel('Biomass loss [tonnes]')
ax1b.scatter(-resF[:, 1], -resF[:, 2]) #, s=30, fc='none', ec='k')
ax1b.set_title('objective space / pareto front')
ax1b.set_xlabel('Biomass loss [tonnes]')
ax1b.set_ylabel('Average distance to protected area [km]')
ax1c.scatter(-resF[:, 0], -resF[:, 2]) #, s=30, fc='none', ec='k')
ax1c.set_title('objective space / pareto front')
ax1c.set_xlabel('Total yield [€]')
ax1c.set_ylabel('Average distance to protected area [km]')
plt.savefig(default_directory + "/figures/objective_space.png")
# plt.show()

# find maxima and add them for colouring
leg = []
percent = 0.05
max_0 = max(-resF[:, 0])
min_0 = min(-resF[:, 0])
quant_0 = max_0 - (max_0 - min_0) * percent
print("min, max, quant")#
print(max_0, min_0, quant_0)
max_1 = max(-resF[:, 1])
min_1 = min(-resF[:, 1])
quant_1 = max_1 - (max_1 - min_1) * percent
max_2 = max(-resF[:, 2])
min_2 = min(-resF[:, 2])
quant_2 = max_2 - (max_2 - min_2) * percent
for i in list(range(0,len(resF))):
    if -resF[i, 0] > quant_0:
        leg.append("0")
    elif -resF[i, 1] > quant_1:
        leg.append("1")
    elif -resF[i, 2] > quant_2:
        leg.append("2")
    else:
        leg.append("x")



# Plot of 3D pareto front; saved as HTML
fig = px.scatter_3d(resF, -resF[:, 0], -resF[:, 1], -resF[:, 2],
                    labels={'x':'Total yield [€]', 'y':'Biomass loss [tonnes]', 'z':'Average distance to protected area [km]'},
                    color = leg)
fig.update_layout(
    title={
        'text': "Pareto Front",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 30
    }
)
fig.write_html(default_directory + "/figures/objective_space_3d.html")
fig.show()



# add here the generations you want to see in the plot
generations2plot = [25, 50, 100, 250, 500, 1000, 1500, 2000]#, 3500, 5000]

# create an empty list to save objective values per generation
# f = []
# # iterate over the generations
# for generation in resHist:
#     # retrieve the optima for all objectives from the generation
#     opt = generation.opt
#     this_f = opt.get("F")
#     f.append(this_f)

n_gen = np.array(range(1, len(f) + 1))

# make the plot
fig4, (ax4a, ax4b, ax4c) = plt.subplots(1, 3, figsize=(15, 5))
# i - 1, because generation 1 has index 0
for i in generations2plot:
    ax4a.scatter(-f[i - 1][:, 0], -f[i - 1][:, 1])
    ax4b.scatter(-f[i - 1][:, 1], -f[i - 1][:, 2])
    ax4c.scatter(-f[i - 1][:, 0], -f[i - 1][:, 2])
ax4a.set_xlabel('Total yield [€]')
ax4a.set_ylabel('Biomass loss [tonnes]')
ax4a.set_xlabel('Biomass loss [tonnes]')
ax4a.set_ylabel('Average distance to protected area [km]')
ax4a.set_xlabel('Total yield [€]')
ax4a.set_ylabel('Average distance to protected area [km]')
plt.legend(list(map(str, generations2plot)))
plt.savefig(default_directory + "/figures/pareto_front_over_generations.png")
# plt.show()
# f3.show()


### 3D plot of the pareto fronts over generations
df = []
for i in generations2plot:
    gen = f[i-1]
    for j in list(range(0, len(gen))):
        x = np.append(gen[j], int(i))
        x = x.tolist()
        df.append(x)
df = np.array(df)
legend = df[:, 3].astype(int).astype(str)

fig = px.scatter_3d(df, -df[:, 0], -df[:, 1], -df[:, 2],
                    labels={'x':'Total yield [€]', 'y':'Biomass loss [tonnes]', 'z':'Average distance to protected area [km]'},
                    color = legend)
fig.update_layout(
    legend_title_text = "Generation",
    legend_title_font_size = 20,
    title={
        'text': "Pareto Front over generations",
        'x': 0.5,
        'xanchor': 'center',
        'font_size': 30
    }
)
fig.write_html(default_directory + "/figures/pareto_fronts_3d.html")
fig.show()


#############################
### Convergence tests


# get maximum (extremes) of each generation for both objectives
obj_1 = []
obj_2 = []
obj_3 = []
for i in f:
    max_obj_1 = min(i[:, 0])
    max_obj_2 = min(i[:, 1])
    max_obj_3 = min(i[:, 2])

    obj_1.append(max_obj_1)
    obj_2.append(max_obj_2)
    obj_3.append(max_obj_3)

# visualize the maxima against the generation number
f3, (ax3a, ax3b, ax3c) = plt.subplots(1, 3, figsize=(15, 5))
ax3a.plot(n_gen, -np.array(obj_1))
ax3a.set_xlabel("Generation")
ax3a.set_ylabel("Maximum total yield [€]")
ax3b.plot(n_gen, -np.array(obj_2))
ax3b.set_xlabel("Generation")
ax3b.set_ylabel("Above ground biomass [tonnes]")
ax3c.plot(n_gen, -np.array(obj_3))
ax3c.set_xlabel("Generation")
ax3c.set_ylabel("Average distance to protected areas [km]")
plt.savefig(default_directory + "/figures/objectives_over_generations.png")
# plt.show()



# TODO: adjust Hypervolume; doesnt work yet

from pymoo.performance_indicator.hv import Hypervolume

# make an array of the generation numbers
n_gen = np.array(range(1, len(f) + 1))
# set reference point
ref_point = np.array([0.0, 0.0])
# create the performance indicator object with reference point
metric = Hypervolume(ref_point=ref_point, normalize=False)
# calculate for each generation the HV metric
hv = [metric.calc(i) for i in f]

# visualze the convergence curve
fig5, ax5 = plt.subplots(1)
ax5.plot(n_gen, hv, '-o', markersize=4, linewidth=2)
ax5.set_xlabel("Generation")
ax5.set_ylabel("Hypervolume")
plt.savefig(default_directory + "/figures/hypervolume.png")
# plt.show()
