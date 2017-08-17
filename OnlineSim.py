import requests
import json
from time import sleep

class OnlineSim:
    def __init__(self):
        self.api_url = "http://onlinesim.ru/api"
        self.headers = {"accept": "application/json"}
        self.api_key = ["xxxxxx"] #your api_key here
        self.LastJson = None

    def SendRequest(self, endpoint):
        self.session = requests.Session()
        self.session.headers.update ({"accept": "application/json"})

        response = self.session.get(self.api_url + endpoint)
        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            print ("Request return " + str(response.status_code) + " error!")
            try:
                self.LastResponse = response
                self.LastJson = json.loads(response.text)
                logging.debug(self.LastJson)
            except:
                pass
            return False

    def getAccount(self, api_key, service):
        self.SendRequest("/getNum.php?apikey=" + api_key + "&service=" + service)
        if str(self.LastJson['response']) == 'TRY_AGAIN_LATER':
            print("Onlinesim: TRY AGAIN LATER...")
        elif str(self.LastJson['response']) == 'NO_NUMBER':
            print("Onlinesim: NO NUMBER...")
        elif str(self.LastJson['response']) == 'EXCEEDED_CONCURRENT_OPERATIONS':
            print("Onlinesim: EXCEEDED CONCURRENT OPERATIONS...")
            sleep(1)
        elif str(self.LastJson['response']) == 'TIME_INTERVAL_ERROR':
            print("Onlinesim: TIME INTERVAL ERROR")
            sleep(1)

        elif self.LastJson['response'] == 1:
            tzid = int(self.LastJson['tzid'])
            print("Onlinesim: Received number. Operation #" + str(tzid))
            return tzid
            
        else: print(self.LastJson['response'])

    def getFeed(self, api_key):
        return self.SendRequest("/getState.php?apikey=" + api_key)

    def getSms(self, api_key, num):
        self.SendRequest("/getState.php?apikey=" + api_key)
        account = list(filter(lambda account: str(account.get('number')) == num, list(self.LastJson)))[0]
        return str(account['msg'])

    def getState(self, api_key, tzid):
        self.SendRequest("/getState.php?apikey=" + api_key)
        account = list(filter(lambda account: int(account.get('tzid')) == tzid, list(self.LastJson)))[0]
        return str(account['response'])

    def getNumber(self, api_key, tzid):
        self.SendRequest("/getState.php?apikey=" + api_key)
        account = list(filter(lambda account: int(account.get('tzid')) == tzid, list(self.LastJson)))[0]
        return str(account['number'])

    def getTzid(self, api_key, num):
        self.SendRequest("/getState.php?apikey=" + api_key)
        account = list(filter(lambda account: str(account.get('number')) == num, list(self.LastJson)))[0]
        return int(account['tzid'])

    def setOperationOk(self, api_key, tzid):
        self.SendRequest("/setOperationOk.php?apikey=" + api_key + "&tzid=" + str(tzid))
        print("Onlinesim: Operation finised:" + str(tzid))

    def setOperationRevise(self, api_key, tzid):
        self.SendRequest("/setOperationRevise.php?apikey=" + api_key + "&tzid=" + str(tzid))
        print("Onlinesim: Revise operation:" + str(tzid))