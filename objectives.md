It's more about the general data structure and not just the objectives.

So my idea was that we in the end just have a table with some columns and every possible mining area as a row / individual. The columns could be the following:
- patch / mining area number: id; do we need one or is the row number enough?
- mining (true / false): indicating if an individual should be mining area or not in this generation (assuming that I understand the mutation and crossover part right..)
- yield (in $ ?): yield value of a given resource (to be researched) * area of the mining cell (can also be preprocessed in GIS or other if we dont manage to do it in Python easily)
- biomass (in tonnes): preprocess by summing up the biomass within a mining area, by assigning biomass to landuse like in tutorial and then just sum the raster cell values / pixel

Then the table could look like this:
|id  |mining  |yield  |biomass |
|---|---|---|---|
|1   |true   |20000   |500   |
|2   |true   |550000   |1200   |

An idea to include the ecological impact (i.e. distance to water / protected area) could be to weight the yield and / or biomass values with the distances, e.g.:
- yield = yield * (distance to nearest protected area / maximum distance of all mining areas in Mato Grosso)

The objective implementation would just be something like:
### yield:
```python
all_yields = []
for mine in mine_list:
  yield = np.where(mining == true, yield, 0)
  tot_yield = np.sum(yield)
  all_yields.append(tot_yield)
```

### similar for biomass, just with:
```python
  biomass = np.where(mining == false, biomass, 0)
```
