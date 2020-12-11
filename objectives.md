It's more about the general data structure and not just the objectives.

So my idea was that we in the end just have a table with some columns and every possible mining area as a row / individual. The columns could be the following:
- patch / mining area number: id; do we need one or is the row number enough?
- mining (true / false): indicating if an individual should be mining area or not in this generation
- yield (in $ ?): yield value of a given resource (to be researched) * area of the mining cell (can also be preprocessed in GIS or other if we dont manage to do it in Python easily)
- biomass (in tonnes): preprocess by summing up the biomass within a mining area, by assigning biomass to landuse like in tutorial and then just sum the raster cell values / pixel

Then the table would look like this:
|id  |mining  |yield  |biomass |
|---|---|---|---|
|1   |true   |20000   |500   |
|2   |true   |550000   |1200   |

Taking into account that our calculation of mining yield needs some flexibility to change it later on, an approach could also look like this:
|id  |mining  |resource  |biomass |area |geometry |
|---|---|---|---|---|---|
|1   |false   |gold   |500   |1000 | geometry... |
|2   |false   |diamonds   |1200   |2000 | geometry... |


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

## Requirements For Input Data
A table-like approach seems feasible, as discussed. We would then need a shapefile as input that fulfills the follfowing cirteria and contains the following information:
- `id`
- `mining_status` for starters, our intput data should only contain mining blocks that are "possible" mining blocks. Blocks that are already established are not considered in our first analysis. The `mining_status` of all of these should be `FALSE`. This is basically our control variable.
- `resource` Type of mined resource, translated if possible
- `area` already in the dataset, unit is important here
- `biomass` The amount of biomass contained in the mining block, in tonnes/ha. A proposed workflow is given below.

### Proposed Workflow for Biomass Estimate

In the end we want to have a summed biomass for each mining block, no matter which land use types with which corresposing biomass amount were present in the input.

The landuse raster

|1 |1 |2 |
|:-:|:-:|:-:|
|1 |2 |2 |
|4 |3 |2 |

with (1 = water, 2 = forest, etc. see tutorial) contains numbers which stand for classes. These numbers could be replaced with the biomass amounts, also given in the tutorial. They are there given in tonnes/ha, but the cell size is actually 6.25 ha. For example water = 0 (obviously), forrest = 300 * 6.25 = 1875. The raster would then be

|0 |0 |1875 |
|:-:|:-:|:-:|
|0 |1875 |1875 |
|? |? |1875 |

If then for each mining polygon the area *sum* of all pixel values in that polygon would be calculated (not the area mean), that would be the value of biomass a mining block contains.