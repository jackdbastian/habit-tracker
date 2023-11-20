library(tidyverse)

setwd('~/apps/music-lib-net-viz/data/')

releases_parsed <- read_csv('parsed/releases.csv')
artists_parsed <- read_csv('parsed/artists.csv')
companies_parsed <- read_csv('parsed/companies.csv')
artists_to_release_parsed <- read_csv('parsed/artists_to_release.csv')
companies_to_release_parsed <- read_csv('parsed/companies_to_release.csv')

releases_clean <- releases_parsed %>% 
  mutate(release_date = str_replace_all(release_date, '-00', '-01')) %>% 
  transmute(
    id = release_id,
    name = release_name,
    release_date = parse_date_time(release_date, c('ymd', 'y')),
    created = Sys.time(),
    updated = Sys.time()
  )

artists_clean <- artists_parsed %>% 
  transmute(
    id = artist_id,
    name = artist_name,
    created = Sys.time(),
    updated = Sys.time()
  )

companies_clean <- companies_parsed %>% 
  transmute(
    id = company_id,
    name = company_name,
    created = Sys.time(),
    updated = Sys.time()
  )

artists_to_release_clean <- artists_to_release_parsed %>%
  mutate(role = strsplit(role, ', ')) %>% 
  unnest(role) %>% 
  mutate(role = str_squish(str_remove(role, '\\[(.*?)\\]'))) %>% 
  transmute(
    id = row_number(),
    artist_id,
    release_id,
    role,
    created = Sys.time(),
    updated = Sys.time()
  )
  
companies_to_release_clean <- companies_to_release_parsed %>% 
  transmute(
    id = row_number(),
    company_id,
    release_id,
    role,
    created = Sys.time(),
    updated = Sys.time()
  )

releases_clean %>% write_csv('cleaned/releases.csv')
artists_clean %>% write_csv('cleaned/artists.csv')
companies_clean %>% write_csv('cleaned/companies.csv')
artists_to_release_clean %>% write_csv('cleaned/artists_to_release.csv')
companies_to_release_clean %>% write_csv('cleaned/companies_to_release.csv')
