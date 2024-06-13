import tkinter as tk
from tkinter import messagebox
from easyocr import Reader
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import pandas as pd
import smtplib
import os
from twilio.rest import Client
from geopy.geocoders import Nominatim
import geocoder
import re

geolocator = Nominatim(user_agent="geoapiExercises")

def get_camera_location():
    try:
        location = geolocator.reverse(g.latlng)
        return location.address
    except Exception as e:
        print('Error:', e)
        return None

g = geocoder.ip('me')
CAMERA_LOCATION = get_camera_location()

def sendSMS(number):
    TWILIO_ACCOUNT_SID = 'ACbb9157657a21259fd7f65f0d11484ba5'
    TWILIO_AUTH_TOKEN = '0840a4c61bbae02fd08c15dd061968f6'
    TWILIO_PHONE_NUMBER = '+18289701273'

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages \
        .create(
            body=f'You were caught riding without helmet near {CAMERA_LOCATION}, and were fined Rupees 500. Please visit https://rzp.io/l/CWHLX4FiCD to pay your due challan. If you are caught riding again without proper gear, you will be severely penalized.',
            from_=TWILIO_PHONE_NUMBER,
            to=f'+{number}'
        )

    print(message.sid)

def sendMail(mail):
    message = MIMEMultipart("alternative")
    message["Subject"] = 'Notification regarding e-challan fine'
    message["From"] = mail
    message["To"] = mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    body = f'You were caught riding without helmet near {CAMERA_LOCATION}, and were fined Rupees 500. Please visit https://rzp.io/l/CWHLX4FiCD to pay your due challan. If you are caught riding again without proper gear, you will be severely penalized.'

    message.attach(MIMEText(body, "plain"))
    server.login('smart.traffic.monitor@gmail.com', 'vimtcznlsxshqyrp')
    server.sendmail('smart.traffic.monitor@gmail.com', mail, message.as_string())
    server.quit()

def notify_violation(licensePlate):
    if licensePlate:
        licensePlate = licensePlate.replace(' ', '')
        licensePlate = licensePlate.upper()
        licensePlate = re.sub(r'[^a-zA-Z0-9]', '', licensePlate)
        print('License number is:', licensePlate)

        if licensePlate in database['Registration'].values:
            index = database.index[database['Registration'] == licensePlate].tolist()[0]
            database.at[index, 'Due challan'] += 500
            mail = database.loc[index, 'Email']
            num = database.loc[index, 'Phone number']
            sendMail(mail)
            sendSMS(num)
            print(f"{database.loc[index, 'Name']} successfully notified!")
            database.to_csv('database.csv', index=False)
        else:
            print("Not Found", "License plate not found in database.")
    else:
        print("No Plate Detected", "No license plate detected.")

database = pd.read_csv('database.csv')

BASE_DIR = 'yolo/runs/detect/exp9/crops/No-helmet'

if __name__ == '__main__':
    for path in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, path).replace('No-helmet', 'Numberplate')
        img = cv2.imread(path, 0)
        reader = Reader(['en'])
        number = reader.readtext(img, mag_ratio=3)
        licensePlate = ""

        for i in [0, 1]:
            for item in number[i]:
                if type(item) == str:
                    licensePlate += item

        notify_violation(licensePlate)
