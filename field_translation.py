import geopandas as gpd
import pandas as pd
import googletrans
from googletrans import Translator
import pydeepl

read_data = gpd.read_file("./../input_data/MinningBlocks/MT.shp")

geodf = gpd.GeoDataFrame(read_data)
geodf_trans = geodf.to_crs(epsg=9001)

translator = Translator()
translations = {}
for column in geodf.columns:

	if column == 'SUBS':
		# Unique elements of the column
		unique_elements = geodf[column].unique()
		print(unique_elements);
		for element in unique_elements:
			# Adding all the translations to a dictionary (translations)
			translations[element] = translator.translate(element).text
print(translations)

geodf.replace(translations, inplace = True)
geodf.head(10)

#print(geodf)

#gdf.to_file("./input_data/MinningBlocks/MT_translated.shp")