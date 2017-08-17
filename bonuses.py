# -*- coding: utf-8 -*-

import sys
import os
import csv
from iocsv import readCSV
from iocsv import writeCSV
from datetime import datetime
from time import sleep
from YoulaAPI import YoulaAPI

def main():
    db_path = os.getcwd() + "\\db_accounts.csv"
    db_file = readCSV(db_path)

    account_cnt = len([x for x in db_file['newCode'] if x == 'Y'])
    print("Avaibale accounts:" + str(account_cnt))

    bonus_code = input('Enter promocode:')
    bonus_cnt = input('Enter amount of account to apply:')

    success_cnt = 0
    cnt = 0
    for i in range(len(db_file['Number'])):
        if db_file["newCode"][i] == 'Y':
            youla = YoulaAPI()
            youla.updateID(db_file["Id"][i])
            youla.updateToken(db_file["Token"][i])

            if youla.applyBonus(bonus_code) == True: success_cnt += 1
            if youla.LastResponse.status_code == 404: print("Incorrect promocode!"); input("Press Enter to exit..."); sys.exit()
            
            cnt += 1
            db_file["newCode"][i] = 'N'
            writeToCSV(db_path, db_file)

            if success_cnt == int(bonus_cnt): break
            sleep(1)

    print("Accounts processed:" + str(cnt))
    print("Accounts processed successfully:" + str(success_cnt))
    print("Bonuses applied successfully:" + str(success_cnt*15))
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()