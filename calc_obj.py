import numpy as np
import geopandas as gpd

# calculate mining yield

def calc_mine_yield(population_array):
    """A function to calculate the yields of a population of mining configurations.
    Input is a population (numpy array) different table configurations"""

    all_yields = []
    # iterate thorugh list of mining blocks
    for candidate in population_array:
        yields = 0

        # TODO TYPE of candidate: np.array or GeoPandasDataFrame? now implemented for dataframe

        # this is for geopandas frame, select mining = TRUE
        # TODO creating a column with true/false results into 1/0 in shp.. investigate
        true_entries = candidate[candidate['mining'] == True]

        # go through rows
        for entry in true_entries:

            # calculate yield
            area = entry['AREA_HA'] * entry['YIELD']
            # add to yield of candidate
            yields = yields + area

        all_yields.append(yields)

        # if status is active, add yield to all_yields
        # if(mining == TRUE) {
        #     yield = area * factor
        #     all_yields.append(yield)
        # }

    return(np.array(all_yields))

# # small testing code, returns area sum
# fp = "./input_data/test_sample/test_sample.shp"
# mines = gpd.read_file(fp)
# print(calc_mine_yield([mines]))

# calculate biomass of mining area
def calc_mine_biomass(population_array):
    """A function to calculate the biomass lost in a collection of mining configurations."""

    biomass_sum = []

    for candidate in population_array:

        biomass = 0

        true_entries = candidate[candidate['mining'] == True]

        for entry in true_entries:
            # TODO: change to entry('biomass')
            # biomass_entry = entry['AREA_HA']
            # distance = entry['distance'] * 10e+06
            # if distance != 0:
            #     biomass_weighted = biomass_entry / distance
            # else:
            #     biomass_weighted = biomass_entry
            biomass_weighted = entry['biomass_to']
            biomass = biomass + biomass_weighted

        biomass_sum.append(biomass)

    return(np.array(biomass_sum))

# test biomass func
# print(calc_mine_biomass([mines]))



# calculate distances to protected areas
def calc_protected_distance(population_array):
    """A function to calculate the average distance of all mining areas to the nearest protected area."""

    distance_sum = []

    for candidate in population_array:

        distances = 0

        true_entries = candidate[candidate['mining'] == True]

        for entry in true_entries:

            distance = entry['distance'] / 1000
            distances = distances + distance

        distance_sum.append(distances/len(true_entries))

    return(np.array(distance_sum))

# test biomass func
# print(calc_mine_biomass([mines]))