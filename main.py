#!/usr/bin/python

import sys
import os
import re
import shlex, subprocess
import httplib2
import pprint
import argparse

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

dirname = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'

USER_CREDS_FILE = dirname + "saved_user_creds.dat"
# Download your credentials from the APIs Console
SECRET_FILE = dirname + "secret_client.json"
# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

storage = Storage(USER_CREDS_FILE)
credentials = storage.get()
if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(SECRET_FILE, OAUTH_SCOPE)
        argparser = argparse.ArgumentParser(add_help=False)
        argparser.add_argument(
                '--noauth_local_webserver', action='store_true',
                default=True, help='Do not run a local web server.'
        )
        argparser.add_argument(
                '--logging_level', default='ERROR',
                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                help='Set the logging level of detail.'
        )
        flags = argparser.parse_args()
        credentials = tools.run_flow(flow, storage, flags)
http = credentials.authorize(httplib2.Http())
drive_service = build("drive", "v2", http)

paths = sys.argv[1:]
regProg = re.compile('^.*\/')
for path in paths:
        filename = regProg.sub('', path)
        print 'Uploading ' + filename + ' ...'
        mimetype = subprocess.Popen(
                "file -b --mime-type " + path, shell=True,
                stdout=subprocess.PIPE
        ).communicate()[0]
        media_body = MediaFileUpload(path, mimetype, resumable=True)
        body = {
                'title': filename
        }
        drive_service.files().insert(body=body, media_body=media_body).execute()
