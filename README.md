# Strix Keylogger

Named after Strix from the Roman occult and folklore, a nocturnal owl that observes and feeds in the dark. Strix is a remote keylogger tool. Running it saves keystrokes to a stream. At regular intervals, the stream is saved to an AES-256 encrypted file "log.txt.aes" and e-mailed to the e-mail address provided.

**Setup:** Run the following command to download dependencies: `pip install requirements.txt`

**Usage:** `strix.py [-h] [-t TIME_INTERVAL] <email> <app_password>`

**Positional arguments:**
  - `email`                 Destination e-mail address where keystrokes and the decryption key are sent to.
  - `app_password`          An app password for authenticating to your mail server. Your E-mail's password does not work. For more information, visit https://support.google.com/accounts/answer/185833?hl=en.

**Options:**
  `-h`, `--help`            show this help message and exit
  `-t`, `--time-interval` TIME_INTERVAL
                        Number of seconds in between sending every other e-mail (default: 60).

**Example:**
```bash
python strix.py "johndoe@gmail.com" "your_app_password_here"
python strix.py "johndoe@gmail.com" "your_app_password_here" -t 60
```

# Known Issues
On Ubuntu, Strix sends e-mails but registers empty keystrokes. As far as I know, this is due to `pynput`'s limited support on Wayland.
This was just my experience trying Strix on Ubuntu, so I do not know how and if this extends to other desktop environments/distributions.
**Trying this on Kali linux works.**

# References
- Tanit Keylogger - [repository](https://github.com/HusseinBakri/Tanit-Keylogger/tree/master)
- Keycodes - [repository](https://github.com/attreyabhatt/Python-Keylogger/blob/master/Keycodes.txt)
- pyAesCrypt - [documentation](https://pypi.org/project/pyAesCrypt/)
- Sending e-mail attachments - [StackOverflow](https://stackoverflow.com/questions/3362600/how-to-send-email-attachments)
- Generating a 32-bit key - [StackOverflow](https://stackoverflow.com/a/70477889)