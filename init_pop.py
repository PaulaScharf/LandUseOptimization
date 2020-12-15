import numpy as np
import geopandas as gpd
import random
import fiona

# make initial population, default_dir is unused
def initialize_spatial(pop_size, default_directory):
    """A function that initializes a population of a given size."""

    all_tables = []
    
    # read the initial dataset (a table with all 'mining' = FALSE)
    table_in = gpd.read_file("./input_data/test_sample/test_sample.shp")

    #table = gpd.GeoDataFrame(table_in)
    #print(table)
    # length of input table
    length = len(table_in)
    
    # make specified number of initializations
    for i in range(pop_size):

        new_table = gpd.GeoDataFrame(table_in)
        new_mining = []

        # new column has same length
        for _ in range(length):
            # append random booleans
            new_mining.append(bool(random.getrandbits(1)))

        # replace the mining column
        new_table['mining'] = new_mining

        table2safe = new_table.to_numpy()
        
        
        all_tables.append(table2safe)

    
    #all_tables = np.array(all_tables.items())
        
        # TODO why are in the final table all 'mining' values the same? 
        # i.e. why and how is the first table appended to all_tables lost?
    # for key in range(all_tables):
    print(all_tables[1][:,11])


    return all_tables

initialize_spatial(2,"path")