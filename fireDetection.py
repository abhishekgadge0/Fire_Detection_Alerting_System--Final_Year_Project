import cv2
import threading
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize Pygame mixer
pygame.mixer.init()

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')
vid = cv2.VideoCapture(0)
runOnce = False
alarm_active = False

def play_alarm_sound_function():
    global alarm_active
    if not alarm_active:
        pygame.mixer.music.load('fire_alarm.mp3')
        pygame.mixer.music.play()
        alarm_active = True

def send_mail_function():
    recipientmail = "s2802989@gmail.com" #remove and write your recipient mail id
    recipientmail = recipientmail.lower()

    subject = "Fire Alert"  # Subject of the email
    message = "Warning: Fire accident has been reported at 18.0339° N, 77.2117° E"  # Body of the email

    try:
        # Create a MIMEText object for the message
        msg = MIMEMultipart()
        msg['From'] = "namithhs118@gmail.com"  #remove and write your sender mail id
        msg['To'] = recipientmail
        msg['Subject'] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()

        # Use your App Password here
        app_password = "lsmc zmdd bqzu jwkh" #remove and write your app password generated from google accout. dont write your email password
        server.login("namithhs118@gmail.com", app_password)  #remove and write your sender mail id

        # Send the email
        server.sendmail('namithhs118@gmail.com', recipientmail, msg.as_string()) #remove and write your sender mail id
        print("Alert mail sent successfully to {}".format(recipientmail))
        server.close()

    except Exception as e:
        print(e)


while True:
    Alarm_Status = False
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()

        if not runOnce:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start()
            runOnce = True

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Stop Pygame mixer and quit
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        break
