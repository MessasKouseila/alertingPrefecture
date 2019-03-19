#!/usr/bin/env python
#  coding: utf-8


# Import Libraries
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:

    def __init__(self, config=None):
        """ Initialisation de la configuration de mailer"""
        self.__config = config
        if self.__config is None:
            with open('config.json') as json_data_file:
                data = json.load(json_data_file)
                self.__config = data['email']
        self.__msg = None

    def send_mail(self, mail_to="messas.kous@gmail.com", subject='ALERTE', content_message=None):
        try:
            self.__msg = MIMEMultipart()
            self.__msg['From'] = self.__config['sender_email']
            self.__msg['To'] = mail_to
            self.__msg['Subject'] = subject
            self.__msg.attach(
                MIMEText(self.__config['default_message'] if content_message is None else content_message))

            server = smtplib.SMTP(self.__config['smtp_server'], self.__config['port'])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.__config['sender_email'], self.__config['password'])
            server.sendmail(self.__msg['From'], self.__msg['To'], self.__msg.as_string())
            server.quit()
            print("ALERTE ENVOYER !!!!!")
        except:
            print("ERROR IN SENDING ALERTE MAIL !!!!!!")
            raise


if __name__ == "__main__":
    mailer = Mailer()
    mailer.send_mail()
