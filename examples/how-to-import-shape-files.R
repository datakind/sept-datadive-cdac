######
# Quick Example of how to import a shape file, transform into a DF, and make a map
# Phil A. 8/2021
#####

packages_needed <- c('tidyverse', 'broom', 'rgdal', 'ggplot2')
for(p in packages_needed){
  library(p, character.only = TRUE)
}

# import from the directory the shapefile is in 
# dsn: directory, layer: name

school_districts <- rgdal::readOGR(dsn = "/Users/philazar/Documents/EDGE_SCHOOLDISTRICT_TL20_SY1920", 
                                   layer = 'EDGE_SCHOOLDISTRICT_TL20_SY1920')

# into a dataframe
school_districts_tidy = tidy(school_districts)

glimpse(school_districts_tidy)

# make a map of entire US 
ggplot(school_districts_tidy, aes(x = long, y = lat, group = group)) +
  geom_polygon(color = "black", size = 0.1, fill = "lightgrey") +
  coord_equal() +
  theme_minimal()

# make a map of only missouri schools using STATE FIPS Code 

# unique id to join 
school_districts$id <- row.names(school_districts)

# left join (just in case id isnt exhaustive, but should be) to get features from data 
sd_with_features <-dplyr::left_join(school_districts_tidy, school_districts@data, by ='id')

# filter using FIPs codes
# you can google FIPS codes for each state's code 
sd_with_features %>% 
  dplyr::filter(STATEFP == 29) %>% 
  ggplot(., aes(x = long, y = lat, group = group)) +
  geom_polygon(color = "black", size = 0.1, fill = "lightgrey") +
  coord_equal() +
  theme_minimal()

