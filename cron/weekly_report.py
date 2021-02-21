import os
import smtplib
import sys
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()


parser = argparse.ArgumentParser()
parser.add_argument("--to", help="Email receipient")
args = parser.parse_args()


def send_email(subject, message, to=[]):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(os.getenv('GMAIL_USER'), os.getenv('GMAIL_PASSWORD'))

    email_text = """\
From: %s 
Subject: %s 

%s
        """ % ("Fiano Monitoring", subject, message)

    server.sendmail("Fiano Monitoring", to, email_text)


if __name__ == '__main__':
    now = datetime.now()
    week_ago = now - timedelta(days=7)

    subject = "Laporan Mingguan {} - {}".format(week_ago.strftime("%d %b %Y"), now.strftime("%d %b %Y"))
    message = "TEST"
    recipients = args.to.split(',')
    send_email(subject, message, recipients)
