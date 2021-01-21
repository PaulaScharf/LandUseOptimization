setwd("/home/petra/Studium/SPAT_OPT/LandUseOptimization")
library(sf)
library(dplyr)

##############################################################
result <- read.csv("./results/result_F1_yield.csv", sep = ",")
result_min <- select(result, c("ID", "mining"))

input <- read_sf("study_areas/study2.shp")

both <- merge(result_min, input, by.X = "ID", by.y = "ID")
both <- st_as_sf(both)
both <- st_zm(both, drop = TRUE)

plot(both["mining"], pal = c("black", "white"))
write_sf(both, "./results/yield.shp")

##############################################################
result <- read.csv("./results/result_F2_biomass.csv", sep = ",")
result_min <- select(result, c("ID", "mining"))

input <- read_sf("study_areas/study2.shp")

both2 <- merge(result_min, input, by.X = "ID", by.y = "ID")
both2 <- st_as_sf(both2)
both2 <- st_zm(both2, drop = TRUE)

plot(both2["mining"], pal = c("black", "white"))
write_sf(both2, "./results/biomass.shp")


##############################################################
result <- read.csv("./results/result_F3_dist.csv", sep = ",")
result_min <- select(result, c("ID", "mining"))

input <- read_sf("study_areas/study2.shp")

both3 <- merge(result_min, input, by.X = "ID", by.y = "ID")
both3 <- st_as_sf(both3)
both3 <- st_zm(both3, drop = TRUE)

plot(both3["mining"], pal = c("black", "white"))
write_sf(both3, "./results/distances.shp")
