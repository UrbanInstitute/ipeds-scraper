library("jsonlite")
library("dplyr")
library("stringr")

allfiles <- fromJSON("data/ipedsfiles.json")

# dataset name
allfiles <- allfiles %>% mutate(urlpart = str_sub(dataurl, start=42, end=-5))
# Get "EF____D" files