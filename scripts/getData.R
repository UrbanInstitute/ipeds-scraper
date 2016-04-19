library("jsonlite")
library("dplyr")
library("stringr")

allfiles <- fromJSON("data/ipedsfiles.json")
datacols <- fromJSON("data/ipedscolumns.json")

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
# f1b01	Tuition and fees, after deducting discounts and allowances
# f2d01	Tuition and fees - Total
vars <- c("f1b01", "f2d01")
dl <- searchVars(vars)
allvars <- tolower(c(vars, "unitid", "year"))
for (i in seq_along(dl)) {
  csvpath <- dl[[i]]$path
  name <- dl[[i]]$name
  d <- read.csv(csvpath, header=T, stringsAsFactors = F)
  # Give it a year variable
  d$year <- dl[[i]]$year
  # All lowercase colnames
  colnames(d) <- tolower(colnames(d))
  # Select just the need vars
  selects <- intersect(colnames(d), allvars)
  d <- d %>% select(one_of(selects))
  
  assign(name, d)
}