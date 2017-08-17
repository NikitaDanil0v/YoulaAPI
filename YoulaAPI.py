#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import uuid
import json
import logging
from random import randint

class YoulaAPI:

    def __init__(self):
        logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'log.log')

        self.api_url = 'https://api.youla.io/api/v1'
        self.device_settings = {'android_version' : 18}
        self.user_agent = 'Youla/2.1.1 (90db330) (Android Version {android_version})'.format(**self.device_settings)
        self.proxy = self.randomProxy()

        self.id = None
        self.name = None
        self.token = None
        self.number = None
        self.LastResponse = None

    def SendRequest(self, endpoint, method, data = None):
        self.session = requests.Session()
        self.session.proxies = {"http" : self.proxy}
        self.session.headers.update ({
                                'X-Auth-Token' : self.token,
                                'Accept-Encoding' : 'gzip, deflate',
                                'User-Agent' : self.user_agent
                                })

        if (method =='get'): # GET
            response = self.session.get(self.api_url + endpoint)
        elif (method == 'post'): # POST
            response = self.session.post(self.api_url + endpoint, data=data)
        elif (method == 'put'): # PUT
            response = self.session.put(self.api_url + endpoint, data=data)

        if response.status_code == 200:
            self.LastResponse = response
            self.LastJson = json.loads(response.text)
            return True
        else:
            print ("Request return " + str(response.status_code) + " error!")
            # debugging
            try:
                self.LastResponse = response
                self.LastJson = json.loads(response.text)
                logging.debug(self.LastJson)
            except:
                pass
            return False

    def generateUUID(self):
        generated_uuid = str(uuid.uuid4().hex)
        return generated_uuid

    def randomName(self):
        f = open(os.getcwd() + "\\female_names.txt", 'r')
        names = f.read().splitlines()
        f = open(os.getcwd() + "\\female_surnames.txt", 'r')
        surnames = f.read().splitlines()
        name = names[randint(0,len(names))]
        surname = surnames[randint(0,len(surnames))]
        logging.debug("Name received:" + name + " " + surname)
        return name, surname        

    def randomProxy(self):
        f = open(os.getcwd() + "\\proxies.txt", 'r')
        proxies = f.read().splitlines()
        i = randint(0, len(proxies)-1)
        proxy = proxies[i]
        logging.debug("Proxy :" + proxy)
        return proxy

    def sendSms(self):
        logging.debug("Sending sms to:" + self.number)
        return self.SendRequest(endpoint="/auth/phone",  method='post', data={"uid": self.uuid, "phone": self.number})

    def confirmAccount(self, sms_code):
        logging.debug("Number confirmation: " + self.number + " - " + "SMS:" + sms_code)
        return self.SendRequest(endpoint="/auth/confirm", method='post', data={"uid": self.uuid, "phone": self.number, "code": sms_code})
        
    def updateNumber(self, num):
        self.number = num
        logging.debug("Number received:" + self.number)

    def updateID(self, id):
        self.id = id
        logging.debug("Id received:" + str(self.id))

    def updateToken(self, token):
        self.token = token
        logging.debug("Token received:" + str(self.token))

    def updateName(self, first_name, last_name):
        self.name = first_name + " " + last_name
        logging.debug("Name changing: " + self.name)
        return self.SendRequest(
            endpoint="/user/" + str(self.id),
            method='put',
            data={"id": str(self.id), "token": str(self.token), "first_name": first_name, "last_name": last_name}
        )

    def applyBonus(self, bonus_code):
        logging.debug("Apply bonuses: " + bonus_code)
        return self.SendRequest(endpoint="/bonus/apply", method='post', data={"bonus_code": bonus_code})