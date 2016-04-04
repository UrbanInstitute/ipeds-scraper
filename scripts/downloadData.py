# -*- coding: utf-8 -*-
"""
Download all the IPEDS data files
Hannah Recht, 04-04-16
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


for i in range(1985,2015):
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

            # Unzip .zips (contain .xlsx dictionaries)
            zip_ref = zipfile.ZipFile(saveurl, 'r')
            zip_ref.extractall("raw/" + str(i) +'/')
            zip_ref.close()

            # Remove zip file
            os.remove("raw/" + str(i) +'/' + urlname)