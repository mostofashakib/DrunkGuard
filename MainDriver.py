import os
import DrugTest
import SpeechToText
import GetAddress
import CallUber

from twilio.rest import Client
# from uber_rides.session import Session
# from uber_rides.client  import UberRidesClient
# from flask import Flask, escape, request, render_template


# app = Flask(__name__)

# @app.route('/')
# def hello():
#      return render_template("index.html")

def send_sms():
    client = Client("KEY_1", "KEY_2")
    content = "Hey, your friend is drunk and needs immediate assistance. Could you please pick the individual up from this location? Location: " + GetAddress.GetAddress_Run()
    client.messages.create(to="NUMBER_1",  from_="NUMBER_2",  body=content)

def OperatingMode():
    DrugTest_Initial = 0

    DrugTest_Initial += DrugTest.DrugTest_Run()

    if DrugTest_Initial == 1:        # only run the second test if the person fails the first one
        DrugTest_Initial += SpeechToText.SpeechToText_Run()

    print(DrugTest_Initial)

    if DrugTest_Initial == 1:
        send_sms()
    elif DrugTest_Initial == 2:
        send_sms()
        print(CallUber.CallUber_Run())
    else:
        print("invalid")

def MainDriverFunction():
    print("Welcome to the drunk test")

    Boolean = int(input('Enter 1 to continue & 0 to exit: ' ))

    if Boolean == 1:
        OperatingMode()
    else:
        print ("Have one see you soon!")

if __name__ == '__main__':
    MainDriverFunction()