import geopandas as gpd
import pandas as pd
#pip install googletrans==3.1.0a0
import googletrans
from googletrans import Translator

read_data = gpd.read_file("./input_data/input_data/MinningBlocks/MT.shp")
read_status = gpd.read_file("./input_data/input_data/MinningBlocks/Brazil_mining_concessions.shp")
read_blocks = gpd.read_file("./Vector/Vector/MiningBlocks/MiningBlocks.shp")

geodf = gpd.GeoDataFrame(read_data)
geodf_status = gpd.GeoDataFrame(read_status)
geodf_status['ID'] = geodf_status['id']
geodf_blocks = gpd.GeoDataFrame(read_blocks)

geodf_blocks['NUMERO'] = geodf_blocks['codigo'].str.slice(7,13)
geodf_blocks['NUMERO'] = pd.to_numeric(geodf_blocks['NUMERO'])
geodf_blocks['ANO'] = geodf_blocks['codigo'].str.slice(14,18)
geodf_blocks['ANO'] = pd.to_numeric(geodf_blocks['ANO'])

geodf = geodf.merge(geodf_blocks[['NUMERO','ANO','leyenda']], on=['NUMERO','ANO'], how='left')
merged_geodf = geodf.merge(geodf_status[['ID','status']], on='ID', how='left')
#geodf_trans = geodf.to_crs("+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +R=6371007.181 +units=m +no_defs +type=crs")
translator = Translator()
translations = {}
for column in merged_geodf.columns:

	if column == 'SUBS' or column == 'USO' or column == 'FASE' or column == 'leyenda':

		# Unique elements of the column
		unique_elements = geodf[column].unique()
		for element in unique_elements:
			if not pd.isnull(element):
				# Adding all the translations to a dictionary (translations)
				translations[element] = translator.translate(element, dest='en').text


print(translations)
merged_geodf.replace(translations, inplace = True)
merged_geodf.head(10)
print(merged_geodf[['SUBS','USO','FASE','status']].head(5))

merged_geodf.to_file("./input_data/input_data/MinningBlocks/MT_translated.shp")
