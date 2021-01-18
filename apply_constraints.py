import numpy as np
import geopandas as gpd
import pandas as pd

def main(df, name):
    df_noUrban = df.loc[df['Urban_Area'] == 0]
    df_noUrban.to_file("./study_areas/" + name + "_noUrban.shp")

    df_noUrban_noProt = df_noUrban.loc[df['distance'] >= 0]
    df_noUrban_noProt.to_file("./study_areas/" + name + "_noUrban_noProt.shp")


print("[INFO] reading first study area")
read_data = gpd.read_file("./study_areas/study1.shp")
geodf = gpd.GeoDataFrame(read_data)
main(geodf, "study1")

print("[INFO] reading second study area")
read_data = gpd.read_file("./study_areas/study2.shp")
geodf = gpd.GeoDataFrame(read_data)
main(geodf, "study2")
