#!/usr/bin/python3
import sys
import os
import re
import subprocess
import argparse

# pydrive reference: https://pythonhosted.org/PyDrive/pydrive.html
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir-id', dest='dirId', help='destination google drive folder id')
parser.add_argument('filepaths', nargs='+', help='files to be upload')
args = parser.parse_args()

# Authentication
# ref: https://stackoverflow.com/a/24542604/2605764
credentialsFilename = 'saved_user_creds.dat'
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

# Upload files
paths = args.filepaths
regProg = re.compile('^.*\/')
for path in paths:
        try:
            filename = regProg.sub('', path)
            print('Uploading ', filename, ' ...')
            file = drive.CreateFile({ 'parents': [{ 'kind': 'drive#fileLink', 'id': args.dirId }] })
            file.SetContentFile(filename)
            file.Upload()
            print('Upload ', filename, ' complete')
        except:
            print("Unexpected error:", sys.exc_info()[0])
