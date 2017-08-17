import sys
import os
from subprocess import Popen, CREATE_NEW_CONSOLE
from sys import executable
import requests
import json
from OnlineSim import OnlineSim
from iocsv import readCSV
from iocsv import writeCSV
import datetime
from time import sleep

def startWorker(api_key, num):
    # Popen([executable, 'worker.py', api_key, num], creationflags=CREATE_NEW_CONSOLE)
    Popen([executable, 'worker.py', api_key, num])
    print("Onlinesim: Worker launched with number:" + num)

def master():
    sim = OnlineSim()

    while True:
        db_workflow = readCSV(os.getcwd() + "\\db_workflow.csv")
        db_accounts = readCSV(os.getcwd() + "\\db_accounts.csv")

        for api_key in sim.api_key:
            tzid = sim.getAccount(api_key, 'Youla')    

        for api_key in sim.api_key:
            sim.getFeed(api_key)
            if sim.LastJson != {'response': 'ERROR_NO_OPERATIONS'}:
                for account in list(sim.LastJson):
                    if str(account['response']) != 'TZ_INPOOL':
                        #In case if something went wrong ;)
                        if (str(account['number']) not in db_workflow['Number']) or (str(account['response']) == 'TZ_NUM_ANSWER' and int(account['time']) <= 900):
                            startWorker(api_key, account['number'])

                            db_workflow['Tzid'].append(account['tzid'])
                            db_workflow['Number'].append(account['number'])
                            db_workflow['DateTime'].append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            
                            writeCSV(os.getcwd() + "\\db_workflow.csv", db_workflow)

                        if str(account['number']) in db_accounts['Number']: sim.setOperationOk(api_key, account['tzid'])
        sleep(1)

if __name__ == '__main__':
    master() 