library("jsonlite")
library("dplyr")
library("stringr")

allfiles <- fromJSON("data/ipedsfiles.json")

# dataset name
allfiles <- allfiles %>% mutate(urlpart = str_sub(dataurl, start=42, end=-5))
# remove the years - the IPEDS names aren't standard but we can try
allfiles <- allfiles %>% mutate(dataname = gsub("\\d", "", allfiles$urlpart))
temp <- as.data.frame(table(allfiles$dataname))
# Get "EF____D" files