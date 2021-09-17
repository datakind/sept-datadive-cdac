library(ooklaOpenDataR)
library(sf)
library(mapview)
library(dplyr)
library(readr)

# Loading U.S. census tract shapefile & aligning coordinate systems with Ookla data's
us_spdf <- sf::read_sf("~/Downloads/cb_2019_us_tract_500k/cb_2019_us_tract_500k.shp")
us_spdf <- sf::st_transform(us_spdf, 4326)
us_spdf <- sf::st_set_crs(us_spdf, 4326)

# Loading all raw Ookla datasets & appending metadata so they can be combined
fixed_tiles_q1 <- ooklaOpenDataR::get_performance_tiles(service = "fixed", year = 2021, quarter = 1, sf = TRUE)
fixed_tiles_q1$type <- "fixed"
fixed_tiles_q1$quarter <- "Q1"
fixed_tiles_q1$year <- 2021

fixed_tiles_q2 <- ooklaOpenDataR::get_performance_tiles(service = "fixed", year = 2021, quarter = 2, sf = TRUE)
fixed_tiles_q2$type <- "fixed"
fixed_tiles_q2$quarter <- "Q2"
fixed_tiles_q2$year <- 2021

mobile_tiles_q1 <- ooklaOpenDataR::get_performance_tiles(service = "mobile", year = 2021, quarter = 1, sf = TRUE)
mobile_tiles_q1$type <- "mobile"
mobile_tiles_q1$quarter <- "Q1"
mobile_tiles_q1$year <- 2021

mobile_tiles_q2 <- ooklaOpenDataR::get_performance_tiles(service = "mobile", year = 2021, quarter = 2, sf = TRUE)
mobile_tiles_q2$type <- "mobile"
mobile_tiles_q2$quarter <- "Q2"
mobile_tiles_q2$year <- 2021

# Function to do the filtering, combining, and writing to disk
prepare_state_data <- function(state_fips_code, state_abbr, save_dir = "~/Downloads/ookla/"){
  
  # Specify spatial data frame
  spdf <- us_spdf %>% dplyr::filter(STATEFP == state_fips_code) # eval(parse(text = paste0(state_fips_code, state_abbr, "_spdf")))
  
  # Filter each of the separate Ookla datasets to the state, combine everything, then merge with spatial df
  q1_fixed_temp <- fixed_tiles_q1 %>% ooklaOpenDataR::filter_by_quadkey(bbox = sf::st_bbox(spdf)) 
  q2_fixed_temp <- fixed_tiles_q2 %>% ooklaOpenDataR::filter_by_quadkey(bbox = sf::st_bbox(spdf)) 
  q1_mobile_temp <- mobile_tiles_q1 %>% ooklaOpenDataR::filter_by_quadkey(bbox = sf::st_bbox(spdf))
  q2_mobile_temp <- mobile_tiles_q2 %>% ooklaOpenDataR::filter_by_quadkey(bbox = sf::st_bbox(spdf)) 
 
  combined_temp <- rbind(q1_fixed_temp, q2_fixed_temp, q1_mobile_temp, q2_mobile_temp)
  combined_temp <- sf::st_join(combined_temp, spdf, join = st_nearest_feature, left = T) %>% dplyr::select(-c(tile))
  
  # Writing spatial data file and combined datasets to disk
  sf::st_write(spdf, paste0(save_dir, state_abbr, "_spdf.shp"))
  readr::write_csv(combined_temp, paste0(save_dir, "ookla_combined_", state_abbr, ".csv"), na = "")
}

# Preparing for 8 states
prepare_state_data("12", "fl")
prepare_state_data("06", "ca")
prepare_state_data("17", "il")
prepare_state_data("22", "la")
prepare_state_data("32", "nv")
prepare_state_data("36", "ny")
prepare_state_data("48", "tx")
prepare_state_data("53", "wa")
