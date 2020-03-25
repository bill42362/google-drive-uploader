#!/usr/bin/python3
import sys
import os
import re
import subprocess

# pydrive reference: https://pythonhosted.org/PyDrive/pydrive.html
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

credentialsFilename = 'saved_user_creds.dat'

# ref: https://stackoverflow.com/a/24542604/2605764
gauth = GoogleAuth()
gauth.LoadCredentialsFile(credentialsFilename)
if gauth.credentials is None:
    gauth.CommandLineAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile(credentialsFilename)

drive = GoogleDrive(gauth)

paths = sys.argv[1:]
regProg = re.compile('^.*\/')
for path in paths:
        try:
            filename = regProg.sub('', path)
            print('Uploading ', filename, ' ...')
            file = drive.CreateFile()
            file.SetContentFile(filename)
            file.Upload()
            print('Upload ', filename, ' complete')
        except:
            print("Unexpected error:", sys.exc_info()[0])
