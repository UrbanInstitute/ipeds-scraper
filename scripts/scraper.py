# -*- coding: utf-8 -*-
"""
Scrape IPEDS http://nces.ed.gov/ipeds/datacenter/DataFiles.aspx
Hannah Recht, 03-24-16
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json

driver = webdriver.Firefox()

# Directory url for downloads
dirurl = "http://nces.ed.gov/ipeds/datacenter/"

files = list()

def scrapetable():
    # Scrape table of datasets
    content = driver.page_source
    soup = BeautifulSoup(''.join(content), "lxml")
    table = soup.find("table", { "id" : "contentPlaceHolder_tblResult" })
    # Get info and URLs for data zip and dictionary zip
    for row in table.find_all('tr')[2:]:
        entry = dict()
        tds = row.find_all('td')
        entry['year'] = int(tds[0].text)
        entry['survey'] = tds[1].text
        entry['title'] = tds[2].text
        entry['dataurl'] = dirurl + tds[3].a.get('href')
        entry['dicturl'] = dirurl + tds[6].a.get('href')
        files.append(entry)

# There is no direct link to the complete data files view. Need to press some buttons.
# If the site changes this will probably all break yay

# Complete data files entry point
driver.get('http://nces.ed.gov/ipeds/datacenter/login.aspx?gotoReportId=7')

# Press continue
driver.find_element_by_xpath("//input[@id='ImageButton1' and @title='Continue']").click()

# Make a list for all the available years
select = Select(driver.find_element_by_id('contentPlaceHolder_ddlYears'))
years = list()
for option in select.options:
    years.append(option.get_attribute('value'))

# Get info on all the available datasets per year, save
def chooseyear(year):
    # Choose year from dropdown
    select.select_by_value(year)
    # Continue to list of datasets
    driver.find_element_by_xpath("//input[@id='contentPlaceHolder_ibtnContinue']").click()
    # Scrape the table of available datasets, add to 'files'
    scrapetable()

# -1 = All years
chooseyear('-1')

# Export to json
with open('data/ipedsfiles.json', 'w') as fp:
    json.dump(files, fp)
