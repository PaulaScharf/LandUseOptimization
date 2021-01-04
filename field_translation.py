import geopandas as gpd
import pandas as pd

read_data = gpd.read_file("./input_data/MinningBlocks/MT.shp")
new_data = pd.read_csv("./input_data/table_translated.csv", encoding='latin1')

geodf = gpd.GeoDataFrame(read_data)
geodf_trans = geodf.to_crs(epsg=9001)
df= pd.DataFrame(new_data)
df['geometry'] = geodf_trans['geometry']
geodf = df
gdf = gpd.GeoDataFrame(geodf, geometry='geometry')

print(gdf['PHASE'])
gdf.to_file("./input_data/MinningBlocks/MT_translated.shp")