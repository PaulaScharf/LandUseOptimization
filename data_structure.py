import numpy as np
import geopandas as gpd
import random
import fiona
import matplotlib as plt


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
	
	print(df_mixed['geometry'])

	df_mixed['biomass_tot'] = df['biomass'] * (df_mixed['geometry'].area / 10**4)

	return df_mixed['ID','biomass_tot'].groupby(by=['ID']).sum()

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

	#** Writing FILTERED DATA dataset (Just Rows with yield column) **
	StAr1_data.to_file("./study_areas/study1.shp")
	StAr2_data.to_file("./study_areas/study2.shp")

	#** Writing TOP LEVEL dataset **
	#df.to_File("./study_areas/TopLevel.shp")

def structure(data):
	# **Reading LandUse Areas**
	read_landUse = gpd.read_file("./../input_data/LandUse/LandUse.shp")
	landUse =  gpd.GeoDataFrame(read_landUse, geometry='geometry')
	# **Reading Protected Areas**
	read_protectedAreas = gpd.read_file("./../input_data/ProtectedAreas/ProtectedAreas.shp")
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
	#print(df['distance'])

	#**Defining True and False THINGS TO CLARIFY**
	df['minning'] = 'true'
	df.loc[df['status'] == 'Available', 'minning'] = 'false'
	df.loc[df['status'] == 'In application', 'minning'] = 'false'
	df.loc[df['status'] == 'Unknown', 'minning'] = 'false'

	#** Calcularion Urban Areas **
	urban_areas =  landUse.loc[landUse['gridcode'] == 11]
	df['Urban_Area'] =  df.intersects(urban_areas.unary_union).astype(bool);

	#Normalizing Mineral Names and Adding Yield Values (GOLD,COPPER, GRAVEL, IRON, SAND)

	df.loc[df['SUBS'].str.contains('GOLD'),['SUBS', 'YIELD']] = ['GOLD', 60328.63 ]
	df.loc[df['SUBS'].str.contains('COPPER'),['SUBS', 'YIELD']] = ['COPPER',7.77]
	df.loc[df['SUBS'].str.contains('IRON'),['SUBS', 'YIELD']] = ['IRON',0.15535]
	df.loc[df['SUBS'] =='GRAVEL',['SUBS', 'YIELD']] = ['GRAVEL',0.00929]
	df.loc[df['SUBS'] =='SAND',['SUBS', 'YIELD']] = ['SAND',0.00929]

	# Selecting Mining Zones with all the values
	new_df =  df[df['YIELD'].notnull()]
	print(new_df.columns)

	# Calculating Biomass 

	biomass = calc_biomass(new_df,landUse)

	print(biomass)

	# Adding the Biomass to the Dataset

	merged_df = new_df.merge(biomass, on='ID')

	saving_finalFiles(df,merged_df)

# Initializing the  Functions
read_data = gpd.read_file("./../input_data/MinningBlocks/MT_translated.shp")

geodf = gpd.GeoDataFrame(read_data)
structure(geodf)