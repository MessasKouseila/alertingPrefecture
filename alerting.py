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
        self.number_try = 0
        self.number_alert = 0

    def do_post(self):
        try:
            self.number_try += 1
            r = requests.post(self.__config['url'], headers=self.__config['headers'], data=self.__config['params'])
            s = self.__config['regex']
            result = re.search(s, r.content.decode('utf-8'))
            # On a trouver le message indiquant qu'il n'existe aucun rendez-vous disponible
            if result is not None:
                print(result.group(0))
                print("###########    UN RENDEZ-VOUS DISPONIBLE    ###########")
                f = open("logAlerte/alerte_" + str(self.number_alert) + ".html", "w+")
                f.write(r.content.decode('utf-8'))
                f.close()
                return True
            else:
                print("###########    AUCUN RENDEZ-VOUS DISPONIBLE    ###########")
                return False
        except:
            print("ERREUR LORS DE L'ACCESS AU SITE DE LA PREFECTURE")
            raise

    def alerting(self):
        while True:
            if self.do_post():
                self.mailer.send_mail("logAlerte/alerte_" + str(self.number_alert) + ".html")
                self.add_number_alert()

            print("###########    TENTATIVE NUMERO                %s     ###########" % self.number_try)
            print("###########    NOUVELLE TENTATIVE DANS %s SECONDES    ###########" % self.__config['time'])
            time.sleep(self.__config['time'])

    def add_number_alert(self):
        self.number_alert += 1
        if self.number_alert > self.__config['max_alert'] - 1:
            exit(0)


if __name__ == "__main__":
    alerter = Alerting()
    alerter.alerting()
