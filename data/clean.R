library(tidyverse)

setwd('~/apps/music-lib-net-viz/data/')

releases_parsed <- read_csv('parsed/releases.csv')
artists_to_release_parsed <- read_csv('parsed/artists_to_release.csv')

releases_clean <- releases_parsed %>% 
  mutate(release_date = str_replace_all(release_date, '-00', '-01')) %>% 
  mutate(release_date = parse_date_time(release_date, c('ymd', 'y')))

artists_to_release_clean <- artists_to_release_parsed %>%
  mutate(role = strsplit(role, ', ')) %>% 
  unnest(role) %>% 
  mutate(role = str_squish(str_remove(role, '\\[(.*?)\\]')))
  
releases_clean %>% write_csv('cleaned/releases.csv')
artists_to_release_clean %>% write_csv('cleaned/artists_to_release.csv')
