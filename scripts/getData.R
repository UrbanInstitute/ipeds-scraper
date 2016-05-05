library("jsonlite")
library("dplyr")
library("stringr")

#Set your directory path for the data, if needed
ipedspath <- "/Users/hrecht/Documents/ipeds-scraper/"

allfiles <- fromJSON(paste(ipedspath, "data/ipedsfiles.json", sep=""))
datacols <- fromJSON(paste(ipedspath, "data/ipedscolumns.json", sep=""))

# Join colnames to file info, remove FLAGS datasets
ipeds <- left_join(datacols, allfiles, by = c("name", "year"))
ipeds <- ipeds %>% filter(!grepl("flags", name))

# Search for a variable, return list of files that contain it
searchVars <- function(vars) {
  # Filter the full IPEDS metadata dataset info to just those containing your vars
  dt <- ipeds %>% filter(grepl(paste(vars, collapse='|'), columns, ignore.case = T))
  dl <- split(dt, dt$name)
  return(dl)
  # For all the files, read in the CSVs
  #dat <- lapply(dt$path, function(i){
  #  read.csv(i, header=T, stringsAsFactors = F)
  #})
  #names(dat) <- dt$name
}

# Example
# f2d01	Tuition and fees - Total
vars <- "f2d01"
dl <- searchVars(vars)
allvars <- tolower(c(vars, "unitid", "year"))
for (i in seq_along(dl)) {
  csvpath <- dl[[i]]$path
  fullpath <- paste(ipedspath, csvpath, sep="")
  name <- dl[[i]]$name
  d <- read.csv(fullpath, header=T, stringsAsFactors = F)
  # Give it a year variable
  d$year <- dl[[i]]$year
  # All lowercase colnames
  colnames(d) <- tolower(colnames(d))
  # Select just the need vars
  selects <- intersect(colnames(d), allvars)
  d <- d %>% select(one_of(selects))
  
  assign(name, d)
}

# If desired, bind the datasets together
makeDataset <- function(vars) {
  dt <- ipeds %>% filter(grepl(paste(vars, collapse='|'), columns, ignore.case = T))
  ipeds_list <- lapply(dt$name, get)
  ipedsdata <- bind_rows(ipeds_list)
  ipedsdata <- ipedsdata %>% arrange(year, unitid)
  return(ipedsdata)
}
ipedsdata <- makeDataset(vars)