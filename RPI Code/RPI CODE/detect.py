from gpiozero import MotionSensor
from picamera import PiCamera
import datetime
from time import sleep
from signal import pause
import storeFileFB
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import BlynkLib
import logging
from dotenv import dotenv_values

#load MQTT configuration values from .env file
config = dotenv_values(".env")
# initialize Blynk
blynk = BlynkLib.Blynk(config['BLYNK_AUTH'])
#configure Logging
logging.basicConfig(level=logging.INFO)

pir = MotionSensor(4)
camera = PiCamera()
camera.rotation = 180
camera.start_preview()
frame = 1

def motionDetected():
    logging.info("Motion Detected")
    blynk.virtual_write(0, 1)
    time = datetime.datetime.now().strftime("%H:%M:%S")
    blynk.log_event("motiondetected", f"Somebody has entered the room at {time}")

def motionNotDetected():
    logging.info("Motion Not Detected")
    blynk.virtual_write(0, 0)

pir.when_motion = motionDetected
pir.when_no_motion = motionNotDetected

# Send an email with an attachment using SMTP
def send_mail(eFrom, to, subject, text, attachment):
    # SMTP Server details: update to your credentials or use class server
    smtpServer='smtp.mailgun.org'
    smtpUser='postmaster@sandboxf2da3229355440ccbc5091fd29afccae.mailgun.org'
    smtpPassword='21b47e85ef2044fea8c150492dc3f156-f2340574-ecc878b2'
    port=587

    # open attachment and read in as MIME image
    fp = open(attachment, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    #construct MIME Multipart email message
    msg = MIMEMultipart()
    msg.attach(MIMEText(text))
    msgImage['Content-Disposition'] = 'attachment; filename="image.jpg"'
    msg.attach(msgImage)
    msg['Subject'] = subject

    # Authenticate with SMTP server and send
    s = smtplib.SMTP(smtpServer, port)
    s.login(smtpUser, smtpPassword)
    s.sendmail(eFrom, to, msg.as_string())
    s.quit()

while True:
    pir.wait_for_motion()
    
    fileLoc = f'/home/pi/assignment2ver4/images/frame{frame}.jpg'
    currentTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    camera.capture(fileLoc)
    print("Motion detected!")
    storeFileFB.store_file(fileLoc)
    storeFileFB.push_db(fileLoc, currentTime)
    print('Image stored and location pushed to db')
    text= f'Hi,\n the attached image was taken today at {currentTime}'
    send_mail('myPi@myhouse.ie', '20062924@mail.wit.ie', 'Intruder Alert',text, fileLoc)
    print('Email Sent')
    blynk.run()
    frame += 1
    pir.wait_for_no_motion()
    camera.stop_preview()