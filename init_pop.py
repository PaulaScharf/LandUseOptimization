import numpy as np
import geopandas as gpd
import random

# make initial population, default_dir is unused
def initialize_spatial(pop_size, default_directory):
    """A function that initializes a population of a given size."""

    all_tables = []
    
    # read the initial dataset (a table with all 'mining' = FALSE)
    table_in = gpd.read_file("./input_data/test_sample/test_sample.shp")

    # length of input table
    length = len(table_in)
    
    # make specified number of initializations
    for _ in range(pop_size):

        new_table = table_in
        new_mining = []

        # new column has same length
        for _ in range(length):
            # append random booleans
            new_mining.append(bool(random.getrandbits(1)))

        # replace the mining column
        new_table['mining'] = new_mining
        all_tables.append(new_table)
        
        # TODO why are in the final table all 'mining' values the same? 
        # i.e. why and how is the first table appended to all_tables lost?
        print(all_tables)

    # print(all_tables)
    return np.array(all_tables)


initialize_spatial(2,"path")