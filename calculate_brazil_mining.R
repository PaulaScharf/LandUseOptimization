# data from: https://www.gov.br/anm/pt-br/assuntos/acesso-a-sistemas/sistema-de-informacoes-geograficas-da-mineracao-sigmine
# setwd()
library(sf)
library(tidyverse)

brazil <- read_sf("./brasil/BRASIL.shp") # read above mentioned data
head(brazil)

unique(brazil$FASE)

lic <- brazil%>% filter(FASE %in% c("APTO PARA DISPONIBILIDADE", "CONCESSÃO DE LAVRA",
                                    "LICENCIAMENTO", "DISPONIBILIDADE",
                                    "AUTORIZAÇÃO DE PESQUISA"))


subs <- unique(brazil$SUBS) # vector of all substances
subs[grep("OURO", subs)] # list substances that contain "OURO"

# gold
ouro <- lic[grep("OURO", lic$SUBS), ] # select all from shp selection
sum(ouro$AREA_HA) # calculate AREA

# gravel
casc <- lic[grep("CASCALHO", lic$SUBS), ]
sum(casc$AREA_HA)

# sand
sand <- lic[grep("AREIA", lic$SUBS), ]
sum(sand$AREA_HA)

# copper
cobr <- lic[grep("COBRE", lic$SUBS), ]
sum(cobr$AREA_HA)

# iron
ferr <- lic[grep("FERRO", lic$SUBS), ]
sum(ferr$AREA_HA)

# diamonds
diam <- lic[grep("DIAMANTE", lic$SUBS), ]
sum(diam$AREA_HA)

##########################################
# data: https://data.globalforestwatch.org/datasets/f6c60c7157f144858521b92bc73160c1_2

gfw <- read_sf("./Brazil_mining_concessions-shp/Brazil_mining_concessions.shp")

exp <- gfw[gfw$status == "Exploitation",]

# gold
ouro <- exp[grep("OURO", exp$subs), ] # select all from shp selection
sum(ouro$area_ha) # calculate AREA

# gravel
casc <- exp[grep("CASCALHO", exp$subs), ]
sum(casc$area_ha)

# sand
sand <- exp[grep("AREIA", exp$subs), ]
sum(sand$area_ha)

# copper
cobr <- exp[grep("COBRE", exp$subs), ]
sum(cobr$area_ha)

# iron
ferr <- exp[grep("FERRO", exp$subs), ]
sum(ferr$area_ha)

# diamonds
diam <- exp[grep("DIAMANTE", exp$subs), ]
sum(diam$area_ha)
