# Hannah Recht, 01-05-16
# Assemble IPEDS dictionaries for use in analyses
# 

library(openxlsx)
library(dplyr)

# Create list of all file paths that we'll need to assemble
paths <- list.files("raw",full.names=T)
paths <- paths[-which(paths=="raw/data")]

dt <- readWorkbook(paths[1], sheet="varlist", colNames=T, rowNames=F)
for (i in paths[-1]) {
  temp <- readWorkbook(i, sheet="varlist", colNames=T, rowNames=F)
  dt <- rbind(dt, temp)
}

dt <- dt %>% arrange(varnumber)
dt$varname <- tolower(dt$varname)
dt$imputationvar <- tolower(dt$imputationvar)

# Remove duplice unitid rows
dt[duplicated(dt),]
dt <- dt[!duplicated(dt),]

# Save to csv
write.csv(dt,"ipeds_dictionary.csv",row.names=F, na="")