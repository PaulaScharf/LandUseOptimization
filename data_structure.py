import numpy as np
import geopandas as gpd
import pandas as pd
import random
import fiona
import matplotlib as plt

print(gpd.show_versions())

def calc_biomass(df,landuse):
	landuse['biomass'] = 0;
	landuse.loc[landuse['gridcode'] == 1, ['new_id','biomass']] = [2,48]
	landuse.loc[landuse['gridcode'] == 2, ['new_id','biomass']] = [6,0]
	landuse.loc[landuse['gridcode'] == 3, ['new_id','biomass']] = [1,300]
	landuse.loc[landuse['gridcode'] == 4, ['new_id','biomass']] = [7,4.69]
	landuse.loc[landuse['gridcode'] == 5, ['new_id','biomass']] = [4,0]
	landuse.loc[landuse['gridcode'] == 6, ['new_id','biomass']] = [4,0]
	landuse.loc[landuse['gridcode'] == 7, ['new_id','biomass']] = [4,0]
	landuse.loc[landuse['gridcode'] == 8, ['new_id','biomass']] = [4,0]
	landuse.loc[landuse['gridcode'] == 9, ['new_id','biomass']] = [4,0]
	landuse.loc[landuse['gridcode'] == 10, ['new_id','biomass']] = [5,16]
	landuse.loc[landuse['gridcode'] == 11, ['new_id','biomass']] = [9,0]
	landuse.loc[landuse['gridcode'] == 12, ['new_id','biomass']] = [8,0]
	landuse.loc[landuse['gridcode'] == 13, ['new_id','biomass']] = [3,150]
	landuse.loc[landuse['gridcode'] == 15, ['new_id','biomass']] = [10,0]

	lu = landuse.to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
	df_mixed = gpd.overlay(lu,df, how= 'identity')
	df_mixed['biomass_tot'] = df_mixed['biomass'] * (df_mixed['geometry'].area / 10**4)
	df_mixed = df_mixed.rename(columns={"ID_1": "ID","biomass_to":"biomass_tot"})

	return df_mixed[['ID','biomass_tot']].groupby(by=['ID']).sum()

def clipping(df):
	## READING AREAS##
	print("[INFO] reading the study area extent")
	read_sa1 = gpd.read_file("./study_areas/study1border.shp")
	read_sa2 = gpd.read_file("./study_areas/study2border.shp")

	StAr1 =  gpd.GeoDataFrame(read_sa1, geometry='geometry').to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
	StAr2 =  gpd.GeoDataFrame(read_sa2, geometry='geometry').to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")

	## CLIPPING AREAS##
	print("[INFO] clipping the mining area to the study area")
	StAr1_data  = gpd.clip(df,StAr1)
	StAr2_data  = gpd.clip(df,StAr2)

	return StAr1_data,StAr2_data

def structuring(df,PAdf_trans,landUse):

	#**Calculating the Area in Hectares**
	print("[INFO] calculating the area in hectares")
	df['Area_Calc'] = df['geometry'].area / 10**4

	#**Measure the Distances**
	print("[INFO] measuring the distance to protected areas")
	df['distance'] = df.geometry.apply(lambda g: PAdf_trans.distance(g).min())
	#print(df['distance'])

	print("[INFO] defining mining status")
	#**Defining True and False THINGS TO CLARIFY**
	df['mining'] = 'true'
	df.loc[df['status'] == 'Available', 'mining'] = 'false'
	df.loc[df['status'] == 'In application', 'mining'] = 'false'
	df.loc[df['status'] == 'Unknown', 'mining'] = 'false'
	df.loc[pd.isnull(df['status']) & df['leyenda'] != 'in operation', 'mining'] = 'false'

	#** Calcularion Urban Areas **
	print("[INFO] checking for urban areas")
	urban_areas =  landUse.loc[landUse['gridcode'] == 11]
	df['Urban_Area'] =  df.intersects(urban_areas.unary_union).astype(bool);

	#Normalizing Mineral Names and Adding Yield Values (GOLD,COPPER, GRAVEL, IRON, SAND)
	print("[INFO] assigning yield")
	df.loc[df['SUBS'].str.contains('GOLD'),['SUBS', 'YIELD']] = ['GOLD', 60328.63 ]
	df.loc[df['SUBS'].str.contains('COPPER'),['SUBS', 'YIELD']] = ['COPPER',7.77]
	df.loc[df['SUBS'].str.contains('IRON'),['SUBS', 'YIELD']] = ['IRON',0.15535]
	df.loc[df['SUBS'] =='GRAVEL',['SUBS', 'YIELD']] = ['GRAVEL',0.00929]
	df.loc[df['SUBS'] =='SAND',['SUBS', 'YIELD']] = ['SAND',0.00929]

	# Selecting Mining Zones with all the values
	print("[INFO] remove items without yield")
	new_df =  df[df['YIELD'].notnull()]

	# Calculating Biomass
	df.to_file("./../input_data/input_data/tempStud1.shp")
	print("[INFO] calculating biomass")
	biomass = calc_biomass(new_df,landUse)

	#print(biomass)

	# Adding the Biomass to the Dataset
	merged_df = new_df.merge(biomass, on='ID')

	return merged_df

def main(data):
	# **Reading LandUse Areas**
	print("[INFO] reading land use raster")
	read_landUse = gpd.read_file("./../input_data/LandUse/LandUse.shp")
	landUse =  gpd.GeoDataFrame(read_landUse, geometry='geometry')
	# **Reading Protected Areas**
	print("[INFO] reading protected areas")
	read_protectedAreas = gpd.read_file("./../input_data/ProtectedAreas/ProtectedAreas.shp")
	# **Creating the GeoDataFrame**
	PAdf =  gpd.GeoDataFrame(read_protectedAreas, geometry='geometry')

	# **Projecting the SHP to 9001 (Same projection as LandUse)**
	print("[INFO] projecting to 9001")
	PAdf_trans = PAdf.to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")

	# **Filtering the Columns**
	print("[INFO] filtering the columns")
	df = data[['ID','FASE','AREA_HA','SUBS','USO','UF','status','geometry','leyenda']].to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")

	stud1, stud2 = clipping(df)
	print("[CRITICAL] structuring the first study area")
	stud1 = structuring(stud1,PAdf_trans,landUse)
	print("[INFO] writing the resulting study area to file")
	stud1.to_file("./study_areas/study1.shp")

	print("[CRITICAL] structuring the second study area")
	stud2 = structuring(stud2,PAdf_trans,landUse)
	print("[INFO] writing the resulting study areas to file")
	stud2.to_file("./study_areas/study2.shp")

# Initializing the  Functions
print("[INFO] reading mining data")
read_data = gpd.read_file("./../input_data/MinningBlocks/MT_translated.shp")

geodf = gpd.GeoDataFrame(read_data)
main(geodf)
