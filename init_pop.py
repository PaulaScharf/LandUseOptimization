import numpy as np
import geopandas as gpd
import random
import fiona

# make initial population, default_dir is unused
def initialize_spatial(pop_size, default_directory):
    """A function that initializes a population of a given size."""

    all_tables = []
    
    # read the initial dataset (a table with all 'mining' = FALSE)
    table_in = gpd.read_file("./Topology/checked_study1_noUrban.gpkg")

    #table = gpd.GeoDataFrame(table_in)
    #print(table)
    # length of input table
    length = len(table_in)
    
    # make specified number of initializations
    for _ in range(pop_size):

        new_table = gpd.GeoDataFrame(table_in)
        new_mining = []

        # new column has same length
        for _ in range(length):
            # append random booleans
            new_mining.append(bool(random.getrandbits(1)))

        # replace the mining column
        new_table['mining'] = new_mining

        # table2safe = new_table.to_numpy()
        # instead, use to_records to preserve df names
        table2safe = new_table.to_records()
                
        all_tables.append(table2safe)

    # column name can be used as follows:
    # print(all_tables[0]["mining"])
    # print(all_tables[0]["mining"][0])

    return all_tables

initialize_spatial(2,"path")