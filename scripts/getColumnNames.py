
# Get column names in each CSV

from urllib.request import urlopen
import json
import os
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("start", help="start year",
                    type=int)
parser.add_argument("stop", help="stop year",
                    type=int)
args = parser.parse_args()

dataVariables = list()
def listVars(start, stop):
    print("*****************************")
    print("Getting column names")
    print("*****************************")
    for i in range(start,stop):
        print("Getting " + str(i) + " column names")
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

listVars(args.start, args.stop)