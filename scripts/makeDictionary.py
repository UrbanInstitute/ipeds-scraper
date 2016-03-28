# -*- coding: utf-8 -*-
"""
Download IPEDS dictionaries and make a master file to index what variables are in what datasets
Hannah Recht, 03-28-16
"""

from urllib.request import urlopen
import json
import zipfile
import os
import xlrd
import csv


# Import json of available files, created in scraper.py
with open('data/ipedsfiles.json') as fp:
    allfiles = json.load(fp)

# Make directory for the raw files
if not os.path.exists('raw/dictionary/'):
    os.makedirs('raw/dictionary/')

def downloadDicts():
    for f in allfiles:
        # URL to download
        url = f['dicturl']
        # dataset file name (XXXX.zip)
        urlname = url.split("http://nces.ed.gov/ipeds/datacenter/data/",1)[1]
        rd = urlopen(url)
        saveurl = "raw/dictionary/" + urlname
        # Save the zip files
        with open(saveurl, "wb") as p:
             p.write(rd.read())
             p.close()

        # Unzip .zips (contain .xlsx dictionaries)
        zip_ref = zipfile.ZipFile(saveurl, 'r')
        zip_ref.extractall("raw/dictionary/")
        zip_ref.close()

        # Remove zip file
        os.remove("raw/dictionary/" + urlname)
downloadDicts()

# The pre-2009 dictionaries are HTML. Fun! Actually misery! 2009+ are mix of .xls and .xlsx
# For the Excel dictionaries, compile the varlist tabs
def makeMasterDict():
    # Set up dictionary CSV
    with open('data/dictionary.csv', 'w') as f:
        c = csv.writer(f)
        c.writerow(['varnumber', 'varname', 'datatype' ,'fieldwidth', 'format', 'imputationvar', 'vartitle', 'dictfile', 'dictname'])

    # For each Excel dictionary, take the contents and file name and add to master dictionary csv
    for file in os.listdir("raw/dictionary/"):
        if file.endswith((".xls", ".xlsx")):
            # print(file)
            dictname = file.split(".", 1)[0]
            workbook = xlrd.open_workbook('raw/dictionary/' + file, on_demand = True)
            worksheet = workbook.sheet_by_name('varlist')
            with open('data/dictionary.csv', 'a') as f:
                c = csv.writer(f)
                for r in range(2,worksheet.nrows):
                    varrow = worksheet.row_values(r)
                    varrow.append(file)
                    varrow.append(dictname)
                    c.writerow(varrow)

makeMasterDict()