# -*- coding: utf-8 -*-
"""
Download all IPEDS  Complete Data Files for a given set of years
Extract and keep final/revised versions
Make a json specifying columns in each data file
Hannah Recht, 04-04-16
"""

from urllib.request import urlopen
import json
import zipfile
import os
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

# Download all the data in given years
def downloadData(start, stop):
    print("*****************************")
    print("Downloading data")
    print("*****************************")
    for i in range(start,stop):
        print("Downloading " + str(i) + " data files")
        # Make directory for the raw files - one per year
        if not os.path.exists('raw/' + str(i) + '/'):
            os.makedirs('raw/' + str(i) + '/')
        # Download all the files in the json
        for f in allfiles:
            if(f['year']==i):
                # URL to download
                url = f['dataurl']
                # dataset file name (XXXX.zip)
                urlname = url.split("http://nces.ed.gov/ipeds/datacenter/data/",1)[1]
                rd = urlopen(url)
                saveurl = "raw/" + str(i) +'/' + urlname
                # Save the zip files
                with open(saveurl, "wb") as p:
                     p.write(rd.read())
                     p.close()

                # Unzip .zips
                zip_ref = zipfile.ZipFile(saveurl, 'r')
                zip_ref.extractall("raw/" + str(i) +'/')
                zip_ref.close()

                # Remove zip file
                os.remove("raw/" + str(i) +'/' + urlname)

# Some datasets have been revised over time, so they'll download XXXX.csv and XXXX_rv.csv
# We only want the revised version
def removeDups(start, stop):
    print("*****************************")
    print("Removing duplicates")
    print("*****************************")
    for i in range(start,stop):
        print("Removing " + str(i) + " duplicates")
        files = os.listdir('raw/' + str(i) + '/')
        # See how many files are in each year
        # print([i,len(files)])
        for file in files:
            # file name minus '.csv'
            name = file[:-4]
            # If the file name ends in _rv, keep that one and delete the other (no _rv)
            if(name[-3:] =='_rv'):
                #print(name)
                unrevised = name[:-3]
                if(os.path.exists('raw/' + str(i) + '/' + unrevised + '.csv')):
                    os.remove('raw/' + str(i) + '/' + unrevised + '.csv')
                    print('Removed ' + unrevised)
#                else:
#                    print('no match ' + unrevised)

downloadData(args.start, args.stop)
removeDups(args.start, args.stop)