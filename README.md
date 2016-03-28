# IPEDS scraper

Get data from IPEDS [complete data files](http://nces.ed.gov/ipeds/datacenter/DataFiles.aspx)

## Run available files scraper:
Assembles json with info on all available complete data files from IPEDS (year, survey, title, data file .zip url, dictionary file .zip url)
```python
pip install selenium
pip install beautifulsoup4
pip install lxml

python3 scripts/scraper.py
```

# Assemble the dictionary
Downloads and extracts all 900 dictionary files from [data/ipedsfiles.json](data/ipedsfiles.json), compiles the .xls and .xlsx ones into [data/dictionary.csv](data/dictionary.csv)
* Note: pre-2009 dictionaries are saved in .html files and aren't parsed here.
```python
pip install xlrd

python3 scripts/makeDictionary.py
```