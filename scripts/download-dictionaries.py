# -*- coding: utf-8 -*-
"""
Scrape IPEDS dictionary ZIP urls save as .txt list
Created on Mon Jan  4 17:10:15 2016
Author: Hannah Recht

"""

# Source: http://nces.ed.gov/ipeds/datacenter/Default.aspx - select complete data files > provisional > 2014

from bs4 import BeautifulSoup
from urllib.request import urlopen
import zipfile
    
url = "/Users/hrecht/Documents/ipeds-dictionary/data/dicttable2014.html"
html_doc = ''.join(open(url,'r').readlines())
soup = BeautifulSoup(html_doc)

# Directory url for downloads
dirurl = "http://nces.ed.gov/ipeds/datacenter/"

zips = list()
t = soup.find_all('table')[0]

# Get contents of href in last column (dictionary urls)
for row in t.find_all('tr')[2:]:
    tds = row.find_all('td')
    url = tds[6].a.get('href')
    # Add full url to list
    zips.append(dirurl + url)
    
    # Save zip files
    dlurl = dirurl + url    
    rd = urlopen(dlurl)
    saveurl = "/Users/hrecht/Documents/ipeds-dictionary/raw/" + url
    with open(saveurl, "wb") as p:
        p.write(rd.read())
        p.close()
    
    # Unzip .zips (contain .xlsx dictionaries)
    zip_ref = zipfile.ZipFile(saveurl, 'r')
    zip_ref.extractall("/Users/hrecht/Documents/ipeds-dictionary/raw/")
    zip_ref.close()

# Print list of urls to .txt file
with open("/Users/hrecht/Documents/ipeds-dictionary/data/dicturls.txt",'w') as f:
    for item in zips:
        f.write("%s\n" % item)
        


