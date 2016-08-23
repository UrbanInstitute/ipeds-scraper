# IPEDS scraper

Get data from IPEDS [complete data files](http://nces.ed.gov/ipeds/datacenter/DataFiles.aspx)

## Scrape list of available files
Assembles [data/ipedsfiles.json](data/ipedsfiles.json) with info on all available complete data files from IPEDS (year, survey, title, data file .zip url, dictionary file .zip url)
```python
python3 scripts/scraper.py
```

## Assemble a master dictionary
Downloads and extracts dictionary files for given years from [data/ipedsfiles.json](data/ipedsfiles.json), compiles the .xls and .xlsx dictionaries into [data/dictionary.csv](data/dictionary.csv)
* Note: pre-2009 dictionaries are saved in .html files and are not parsed here.
```python
python3 scripts/makeDictionary.py STARTYEAR STOPYEAR
```

## Download files
Download data files listed in [data/ipedsfiles.json](data/ipedsfiles.json) for a given range of years.
```python
python3 scripts/downloadData.py STARTYEAR STOPYEAR
```

## Get column names
Get column names from downloaded files for a given range of years and save in a json.
```python
python3 scripts/getColumnNames.py STARTYEAR STOPYEAR
```