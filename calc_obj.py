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
            area = entry['AREA_HA']
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
            area = entry['AREA_HA']
            area = area * 2
            biomass = biomass + area

        biomass_sum.append(biomass)

    return(np.array(biomass_sum))

# test biomass func
# print(calc_mine_biomass([mines]))