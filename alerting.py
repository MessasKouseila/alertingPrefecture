#!/usr/bin/env python
#  coding: utf-8

# Import Libraries
import json
import re
import time
import requests
from mail import Mailer


class Alerting:

    def __init__(self, config=None):
        """ Initialisation de la configuration de l'alerting"""

        self.__config = config
        if self.__config is None:
            with open('config.json') as json_data_file:
                data = json.load(json_data_file)
                self.__config = data['site']

        self.mailer = Mailer()

    def do_post(self):
        try:
            r = requests.post(self.__config['url'], headers=self.__config['headers'], data=self.__config['params'])
            s = self.__config['regex']
            result = re.search(s, r.content.decode('utf-8'))
            # On a trouver le message indiquant qu'il n'existe aucun rendez-vous disponible
            if result:
                print(result.group(0))
                print("###########    AUCUN RENDEZ-VOUS DISPONIBLE    ###########")
                return False
            else:
                print("###########    UN RENDEZ-VOUS DISPONIBLE    ###########")
                return True
        except:
            print("ERREUR LORS DE L'ACCESS AU SITE DE LA PREFECTURE")
    def alerting(self):
        while True:
            if self.do_post():
                self.mailer.send_mail()
            print("###########    NOUVELLE TENTATIVE DANS %s SECONDES    ###########" % self.__config['time'])
            time.sleep(self.__config['time'])


if __name__ == "__main__":
    alerter = Alerting()
    alerter.alerting()
