# IPEDS scraper

Download data from IPEDS [complete data files](http://nces.ed.gov/ipeds/datacenter/DataFiles.aspx). 

For each year, IPEDS splits data into several files - up to several dozen. The datasets are each saved as .csv and compressed into .zip (Stata file .zip are also available). For some years, revised datasets are available. These are included in the same .zip file. In revised file cases, the non-revised file is deleted in scripts/downloadData.py and the final version is saved.

Each file has a corresponding dictionary .zip, which includes .xls, .xlsx, or .html dictionaries. According to NCES, there is no comprehensive dictionary available.

Beware: variable names frequently change between years. In other cases, the variable name will stay the same but the value levels will change (e.g. 1,2,3 in 2000 and 5,10,15,20 in 2001). I don't have a good answer for comparing between years, besides looking at the data dictionaries. If you have a better answer please share!


## Functions
### Scrape list of available files
Assembles [data/ipedsfiles.json](data/ipedsfiles.json) with info on all available complete data files from IPEDS (year, survey, title, data file .zip url, dictionary file .zip url)
```python
python3 scripts/scraper.py
```

### Assemble a master dictionary
Downloads and extracts dictionary files for given years from [data/ipedsfiles.json](data/ipedsfiles.json), compiles the .xls and .xlsx dictionaries into [data/dictionary.csv](data/dictionary.csv)
* Note: pre-2009 dictionaries are saved in .html files and are not parsed here.
```python
python3 scripts/makeDictionary.py STARTYEAR STOPYEAR
```

### Download files
Download data files listed in [data/ipedsfiles.json](data/ipedsfiles.json) for a given range of years.
```python
python3 scripts/downloadData.py STARTYEAR STOPYEAR
```

### Get column names
Get column names from downloaded files for a given range of years and save in a json.
```python
python3 scripts/getColumnNames.py STARTYEAR STOPYEAR
```