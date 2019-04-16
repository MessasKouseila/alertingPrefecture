#!/usr/bin/env python
#  coding: utf-8


# Import Libraries
import json
import smtplib
from email import encoders
from email.mime.base import MIMEBase
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

    def send_mail(self, content_message=None, mail_to="messas.kous@gmail.com", subject='ALERTE'):
        try:
            self.__msg = MIMEMultipart()
            self.__msg['From'] = self.__config['sender_email']
            self.__msg['To'] = self.__config['sender_email_to'] if self.__config[
                                                                       'sender_email_to'] is not None else mail_to
            self.__msg['Subject'] = subject
            self.__msg.attach(
                MIMEText(self.__config['default_message']))
            if content_message is not None:
                # open the file to be sent
                filename = content_message
                attachment = open(content_message, "rb")

                # instance of MIMEBase and named as p
                p = MIMEBase('application', 'octet-stream')

                # To change the payload into encoded form
                p.set_payload(attachment.read())

                # encode into base64
                encoders.encode_base64(p)

                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                # attach the instance 'p' to instance 'msg'
                self.__msg.attach(p)

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
