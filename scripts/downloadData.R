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
  dt <- ipeds %>% filter(grepl(paste(vars, collapse='|'), columns, ignore.case = T))
  return(dt)
}

# Example
# f1b01	Tuition and fees, after deducting discounts and allowances
# f2d01	Tuition and fees - Total
myvars <- c("f1b01", "f2d01")

dt <- searchVars(myvars)
vars <- c(myvars, "unitid")
for (i in 1:nrow(dt)) {
  name <- dt[i,"name"]
  path <- dt[i, "path"]
  assign(name, read.csv(path, stringsAsFactors = F))
}
