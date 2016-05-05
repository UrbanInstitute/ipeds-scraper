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

# Import json of available files, created in scraper.py
with open('data/ipedsfiles.json') as fp:
    allfiles = json.load(fp)

# Download all the data in given years
def downloadData(start, stop):
    print("Downloading data")
    for i in range(start,stop):
        print(i)
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
#downloadData(1985, 2015)

# Some datasets have been revised over time, so they'll download XXXX.csv and XXXX_rv.csv
# We only want the revised version
def removeDups(start, stop):
    print("Removing duplicates")
    for i in range(start,stop):
        print(i)
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
                    print('removed ' + unrevised)
                else:
                    print('no match ' + unrevised)
#removeDups(1985, 2015)


# Get column names in each CSV
dataVariables = list()
def listVars(start, stop):
    print("Getting column names")
    for i in range(start,stop):
        print(i)
        files = os.listdir('raw/' + str(i) + '/')
        for file in files:
            if file.endswith(('.csv')):
                #print(file)

                entry = dict()
                entry['year'] = i

                # file name minus '.csv'
                name = file[:-4]
                # If the file name ends in _rv, strip the rv for name field
                if(name[-3:] =='_rv'):
                    name = name[:-3]

                entry['name'] = name
                entry['path'] = 'raw/' + str(i) + '/' + file
                with open('raw/' + str(i) + '/' + file, 'r') as c:
                    d_reader = csv.DictReader(c)
                    entry['columns'] = d_reader.fieldnames
                c.close()
                dataVariables.append(entry)
    # Export to json
    with open('data/ipedscolumns.json', 'w') as fp:
        json.dump(dataVariables, fp)

listVars(1985, 2015)