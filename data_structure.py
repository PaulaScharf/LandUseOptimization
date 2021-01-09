import numpy as np
import geopandas as gpd
import random
import fiona
import matplotlib as plt



def saving_finalFiles(df, new_df):
	## READING AREAS##
	read_sa1 = gpd.read_file("./study_areas/study1border.shp")
	read_sa2 = gpd.read_file("./study_areas/study2border.shp")

	StAr1 =  gpd.GeoDataFrame(read_sa1, geometry='geometry').to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
	StAr2 =  gpd.GeoDataFrame(read_sa2, geometry='geometry').to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")

	## CLIPPING AREAS##
	
	StAr1_data  = gpd.clip(new_df,StAr1)
	StAr2_data  = gpd.clip(new_df,StAr2)

	## WRITING THE FINAL FILES ##
	
	#** Writing TOP LEVEL dataset **
	#df.to_File("./input_data/TopLevel.shp")

	#** Writing FILTERED DATA dataset (Just Rows with yield column) **
	StAr1_data.to_file("./study_areas/study1.shp")
	StAr2_data.to_file("./study_areas/study2.shp")


def structure(data):
	# **Reading LandUse Areas**
	read_landUse = gpd.read_file("./../input_data/LandUse/LandUse.shp")
	landUse =  gpd.GeoDataFrame(read_landUse, geometry='geometry')
	print(data.columns)
	# **Reading Protected Areas**
	read_protectedAreas = gpd.read_file("./../input_data/ProtectedAreas/ProtectedAreas.shp")
	print(read_protectedAreas['geometry'])
	# **Creating the GeoDataFrame**
	PAdf =  gpd.GeoDataFrame(read_protectedAreas, geometry='geometry')
	
	# **Projecting the SHP to 9001 (Same projection as LandUse)**
	PAdf_trans = PAdf.to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
	
	# **Filtering the Columns**
	df = data[['ID','FASE','AREA_HA','SUBS','USO','UF','status','geometry']].to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
	
	#**Calculating the Area in Hectares**
	df['Area_Calc'] = df['geometry'].area / 10**4

	#**Measure the Distances**
	
	df['distance'] = df.geometry.apply(lambda g: PAdf_trans.distance(g).min())
	print(df['distance'])

	#**Defining True and False THINGS TO CLARIFY**
	df['minning'] = 'true'
	df.loc[df['status'] == 'Available', 'minning'] = 'false'
	df.loc[df['status'] == 'In application', 'minning'] = 'false'
	df.loc[df['status'] == 'Unknown', 'minning'] = 'false'

	#** Calcularion Urban Areas **
	urban_areas =  landUse.loc[landUse['gridcode'] == 11]
	print(urban_areas)
	df['Urban_Area'] = 0

	#Normalizing Mineral Names and Adding Yield Values (GOLD,COPPER, GRAVEL, IRON, SAND)

	df.loc[df['SUBS'].str.contains('GOLD'),['SUBS', 'YIELD']] = ['GOLD', 60328.63 ]
	df.loc[df['SUBS'].str.contains('COPPER'),['SUBS', 'YIELD']] = ['COPPER',7.77]
	df.loc[df['SUBS'].str.contains('IRON'),['SUBS', 'YIELD']] = ['IRON',0.15535]
	df.loc[df['SUBS'] =='GRAVEL',['SUBS', 'YIELD']] = ['GRAVEL',0.00929]
	df.loc[df['SUBS'] =='SAND',['SUBS', 'YIELD']] = ['SAND',0.00929]

	# Selecting Mining Zones with all the values
	new_df =  df[df['YIELD'].notnull()]
	print(new_df['geometry'])



	saving_finalFiles(df,new_df)

# Initializing the  Functions
read_data = gpd.read_file("./../input_data/MinningBlocks/MT_translated.shp")

geodf = gpd.GeoDataFrame(read_data)
structure(geodf)
