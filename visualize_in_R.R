setwd("/home/petra/Studium/spatopt/LandUseOptimization")
library(sf)
library(dplyr)
library(stars)

# load from /results
yield <- read.csv("./results/study1_inverseMut/result_F1_yield.csv", sep = ",")
biomass <- read.csv("./results/study1_inverseMut/result_F2_biomass.csv", sep = ",")
dist <- read.csv("./results/study1_inverseMut/result_F3_dist.csv", sep = ",")

# make into sf data frames
yield$geometry <- as.character(yield$geometry)
yield$geometry <- as.list(yield$geometry)
yield <- st_as_sf(yield)
yield <- st_zm(yield, drop = TRUE)

biomass$geometry <- as.character(biomass$geometry)
biomass$geometry <- as.list(biomass$geometry)
biomass <- st_as_sf(biomass)
biomass <- st_zm(biomass, drop = TRUE)

dist$geometry <- as.character(dist$geometry)
dist$geometry <- as.list(dist$geometry)
dist <- st_as_sf(dist)
dist <- st_zm(dist, drop = TRUE)

# plot
plot(yield["mining"], pal = c("green", "grey"), main="yield")
plot(biomass["mining"], pal = c("green", "grey"), main="biomass")
plot(dist["mining"], pal = c("green", "grey"), main="distance")

write_sf(yield, "./results/study1_inverseMut/best_yield.shp")
write_sf(biomass, "./results/study1_inverseMut/best_bio.shp")
write_sf(dist, "./results/study1_inverseMut/best_dist.shp")

