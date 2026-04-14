import pyAesCrypt
import sys
import io

'''
Summplementary AES decryption script.

Usage: python decrypt.py <Encrypted filename> <Key>

Args:
    - encryptedFile (str): name of the AES-256 encrypted file
    - key (str): 32-bit key

Example:
    python decrypt.py "log.txt.aes" "your_key"
'''

BUFFERSIZE = 64*1024

encryptedFile = sys.argv[1]
key = sys.argv[2]

with open(encryptedFile, "rb") as f:
    encryptedData = f.read()
fIn = io.BytesIO(encryptedData)
fOut = io.BytesIO()
pyAesCrypt.decryptStream(fIn, fOut, key, BUFFERSIZE)
decryptedData = fOut.getvalue()
print(decryptedData.decode('utf-8'))