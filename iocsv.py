# -*- coding: utf-8 -*-
import csv

def writeCSV(path, dict_data):
    try:
        with open(path, 'w', errors='ignore',  newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(dict_data.keys())
            for i in range(len(dict_data['Number'])):
                writer.writerow([dict_data[key][i] for key in dict_data.keys()])
    except IOError as err:
            print("I/O error({0}):".format(err))    
    return

def readCSV(path):
    try:
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            dict_data = {}
            for row in reader:
                for column, value in row.items():
                    dict_data.setdefault(column, []).append(value)
            if dict_data == {}: dict_data = {key:[] for key in reader.fieldnames}
            return dict_data
    except IOError as err:
            print("I/O error({0}):".format(err))    
    return

def appendCSV(path, data):
    try:
        with open(path, 'a', newline='') as f:
            insert = [data[key] for key in ((csv.DictReader(open(path), delimiter=';')).fieldnames)]
            writer = csv.writer(f, delimiter=';')
            writer.writerow(insert)
    except IOError as err:
        print("I/O error({0}):".format(err)) 
    return