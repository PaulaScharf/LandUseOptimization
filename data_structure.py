import numpy as np
import geopandas as gpd
import random
import fiona
import matplotlib as plt

def structure(data):
	df= data[['ID','PHASE','AREA_HA','SUBS','USE','UF','geometry']]
	print(df)




read_data = gpd.read_file("./input_data/MinningBlocks/MT_translated.shp")
geodf = gpd.GeoDataFrame(read_data)
structure(geodf)
