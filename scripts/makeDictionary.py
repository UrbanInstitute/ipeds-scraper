# -*- coding: utf-8 -*-
"""
Download IPEDS dictionaries and make a master csv dictionary
Note, pre-2009 dictionaries are awfully-formatted HTML.
"""

from urllib.request import urlopen
import json
import zipfile
import os
import xlrd
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("start", help="start year",
                    type=int)
parser.add_argument("stop", help="stop year",
                    type=int)
args = parser.parse_args()

# Import json of available files, created in scraper.py
with open('data/ipedsfiles.json') as fp:
    allfiles = json.load(fp)

# Make directory for the raw files
if not os.path.exists('raw/dictionary/'):
    os.makedirs('raw/dictionary/')

# The pre-2009 dictionaries are HTML. Fun! Actually misery! 2009+ are mix of .xls and .xlsx and a few .html
# Downloading the pre-2009 dictionary zips will get you a bunch of html files

def downloadDicts(start, stop):
    print("*****************************")
    print("Downloading dictionaries")
    print("*****************************")
    for i in range(start,stop):
        print("Downloading " + str(i) + " dictionaries")
        # Make directory for the raw files - one per year
        if not os.path.exists('dict/' + str(i) + '/'):
            os.makedirs('dict/' + str(i) + '/')
        # Download all the files in the json
        for f in allfiles:
            if(f['year']==i):
                # URL to download
                url = f['dicturl']
                # dataset file name (XXXX.zip)
                urlname = url.split("http://nces.ed.gov/ipeds/datacenter/data/",1)[1]
                rd = urlopen(url)
                saveurl = "dict/" + str(i) +'/' + urlname
                # Save the zip files
                with open(saveurl, "wb") as p:
                     p.write(rd.read())
                     p.close()

                # Unzip .zips
                zip_ref = zipfile.ZipFile(saveurl, 'r')
                zip_ref.extractall("dict/" + str(i) +'/')
                zip_ref.close()

                # Remove zip file
                os.remove("dict/" + str(i) +'/' + urlname)

# For the Excel dictionaries, compile the varlist tabs
def makeMasterDict(start, stop):
    print("*****************************")
    print("Assembling master dictionary")
    print("*****************************")
    # Set up dictionary CSV
    with open('data/dictionary.csv', 'w') as f:
        c = csv.writer(f)
        c.writerow(['year', 'dictname', 'dictfile', 'varnumber', 'varname', 'datatype' ,'fieldwidth', 'format', 'imputationvar', 'vartitle'])
        f.close()

        # For each Excel dictionary, take the contents and file name and add to master dictionary csv
    for i in range(start,stop):
        for file in os.listdir('dict/' + str(i) + '/'):
            if file.endswith((".xls", ".xlsx")):
                print("Adding " + str(i) + " " + file + " to dictionary")
                dictname = file.split(".", 1)[0]
                rowstart = [i, dictname, file]
                workbook = xlrd.open_workbook('dict/' + str(i) +'/' + file, on_demand = True)
                worksheet = workbook.sheet_by_name('varlist')
                with open('data/dictionary.csv', 'a') as f:
                    c = csv.writer(f)
                    for r in range(2,worksheet.nrows):
                        varrow = worksheet.row_values(r)
                        row = rowstart + varrow
                        c.writerow(row)

downloadDicts(args.start, args.stop)
makeMasterDict(args.start, args.stop)