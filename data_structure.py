import numpy as np
import geopandas as gpd
import random
import fiona
import matplotlib as plt



def saving_finalFiles(df, new_df):
	## WRITING THE FINAL FILES ##
	
	#** Writing TOP LEVEL dataset **
	df.to_File("./input_data/TopLevel.shp")

	#** Writing FILTERED DATA dataset (Just Rows with yield column) **
	new_df.to_file("./input_data/FilteredData.shp")


def structure(data):
	# **Reading Protected Areas**
	read_protectedAreas = gpd.read_file("./../input_data/ProtectedAreas/ProtectedAreas.shp")
	
	# **Creating the GeoDataFrame**
	PAdf =  gpd.GeoDataFrame(read_protectedAreas)
	
	# **Projecting the SHP to 9001 (Same projection as LandUse)**
	PAdf_trans = PAdf.to_crs(epsg=9001)
	
	# **Filtering the Columns**
	df = data[['ID','PHASE','AREA_HA','SUBS','USE','UF','geometry']]
	
	#**Calculating the Area in Hectares**
	df['Area_Calc'] = df['geometry'].area / 10**4

	#**Measure the Distances**
	
	df['distance'] = df.geometry.apply(lambda g: PAdf_trans.distance(g).min())
	print(df['distance'])

	#**Defining True and False THINGS TO CLARIFY**

	#df.loc[df['PHASE'].str.contains('APPLICATION'), 'minning'] = 'false'

	#** Calcularion Urban Areas **

	df['Urban_Area'] = 0

	#Normalizing Mineral Names and Adding Yield Values (GOLD,COPPER, GRAVEL, IRON, SAND)

	df.loc[df['SUBS'].str.contains('GOLD'),['SUBS', 'YIELD']] = ['GOLD', 60328.63 ]
	df.loc[df['SUBS'].str.contains('COPPER'),['SUBS', 'YIELD']] = ['COPPER',7.77]
	df.loc[df['SUBS'].str.contains('IRON'),['SUBS', 'YIELD']] = ['IRON',0.15535]
	df.loc[df['SUBS'] =='GRAVEL',['SUBS', 'YIELD']] = ['GRAVEL',0.00929]
	df.loc[df['SUBS'] =='SAND',['SUBS', 'YIELD']] = ['SAND',0.00929]

	# Selecting Mining Zones with all the values
	new_df =  df[df['YIELD'].notnull()]
	print(new_df)

	saving_finalFiles(df,new_df)

# Initializing the  Functions
read_data = gpd.read_file("./../input_data/MinningBlocks/MT_translated.shp")
geodf = gpd.GeoDataFrame(read_data)
structure(geodf)
