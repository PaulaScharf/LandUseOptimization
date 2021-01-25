setwd("/home/petra/Studium/spatopt/LandUseOptimization")
library(sf)
library(dplyr)
library(stars)

# load from /results
yield <- read.csv("./results/result_F1_yield.csv", sep = ",")
biomass <- read.csv("./results/result_F2_biomass.csv", sep = ",")
dist <- read.csv("./results/result_F3_dist.csv", sep = ",")

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

write_sf(yield, "./results/best_yield.shp")
write_sf(biomass, "./results/best_bio.shp")
write_sf(dist, "./results/best_dist.shp")

##################################################
stu <- read_sf("./study_areas/study2_noUrban.shp")

# x are polygons, y are solutions, such that
# rows are complete solutions
sol <- read.csv("./results/solutions.csv")
per <- read.csv("./results/performances.csv")
per$X0 <- -per$X0
per$X1 <- -per$X1
per$X2 <- -per$X2

# calculate some sort of measure, here: sum
per$sum <- per$X0 + per$X1 + per$X2
# index of best performing candidate is
index <- per[per$sum == max(per$sum),]$X

# its mining vector is
miningBest <- as.vector(sol[index, 2:ncol(sol)])
miningBest <- unname(unlist(miningBest))

# assign to shape
stu$mining <- miningBest

# plot
plot(stu["mining"], pal = c("green", "grey"), main="Best Solution")
