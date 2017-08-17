# -*- coding: utf-8 -*-
import sys
import os
from YoulaAPI import YoulaAPI
from OnlineSim import OnlineSim
from iocsv import readCSV
from iocsv import appendCSV
import datetime
from time import sleep

def main(argv):
    sim = OnlineSim()
    youla = YoulaAPI()
    youla.uuid = youla.generateUUID()

    if argv == []: api_key = input("Enter api_key:"); num = input("Enter Number:")
    else: api_key = argv[0]; num = argv[1]

    print("Number In Process:" + str(num))
    
    youla.updateNumber(num)
    if not youla.sendSms():
        print("Number is incorrect. Program terminated.")
        sim.setOperationOk(api_key, sim.getTzid(api_key, num))
        sleep(3)
        sys.exit()

    print("Number lifetime 20 minutes. Sending SMS each 3 minutes.")
    deadline = datetime.datetime.now() + datetime.timedelta(seconds=180)
    while True:
        if datetime.datetime.now() >= deadline:
            print("Sending SMS.")
            deadline = datetime.datetime.now() + datetime.timedelta(seconds=180)
            youla.sendSms()

        if sim.getState(api_key, sim.getTzid(api_key, num)) == 'TZ_NUM_ANSWER':
            sms_code = sim.getSms(api_key, num)
            print("SMS received:" + sms_code)

            if youla.confirmAccount(sms_code): break
            else: sim.setOperationRevise(api_key, sim.getTzid(api_key, num)); youla.sendSms(); sleep(10)

        sleep(1)

    youla.updateID(youla.LastJson['data']['id'])
    youla.updateToken(youla.LastJson['data']['token'])
    first_name, last_name = youla.randomName()
    youla.updateName(first_name, last_name)

    append = {'Id':youla.id, 'Name':youla.name, 'Token':youla.token, 'Number':youla.number, 'DateTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'newCode':'Y'}
    appendCSV(os.getcwd() + "\\db_accounts.csv", append)

    print("Successful exit...")
    sleep(3)

if __name__ == '__main__':
    main(sys.argv[1:])