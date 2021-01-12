import geopandas as gpd
import pandas as pd
import googletrans
from googletrans import Translator

read_data = gpd.read_file("./../input_data/MinningBlocks/MT.shp")
read_status = gpd.read_file("./../input_data/MinningBlocks/Brazil_mining_concessions.shp")

geodf = gpd.GeoDataFrame(read_data)
geodf_status = gpd.GeoDataFrame(read_status)
geodf_status['ID'] = geodf_status['id']

merged_geodf = geodf.merge(geodf_status[['ID','status']], on='ID')
#geodf_trans = geodf.to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
print(merged_geodf['status'].unique())
translator = Translator()
translations = {}
for column in merged_geodf.columns:

	if column == 'SUBS' or column == 'USO' or column == 'FASE' :

		# Unique elements of the column
		unique_elements = geodf[column].unique()
		print(unique_elements);
		for element in unique_elements:
			# Adding all the translations to a dictionary (translations)
			translations[element] = translator.translate(element).text
print(translations)

merged_geodf.replace(translations, inplace = True)
merged_geodf.head(10)
print(merged_geodf.columns)

#print(merged_geodf[['SUBS','USO','FASE','status']].head(5))


merged_geodf.to_file("./../input_data/MinningBlocks/MT_translated.shp")