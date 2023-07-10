#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#### Below is the official tutorial from https://developers.google.com/sheets/api/quickstart/python

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = Credentials.from_authorized_user_file('token.json', SCOPES)
## If run for the first time, generate the token.json from credentials.json
## This might not be able to do in the server, as it will pop up a web browser asking you to login
## Copy this script and the credentials.json file to your local computer. Run the script and it will generate the token.json
## Copy the token.json back to the server

#if not creds or not creds.valid:
#    if creds and creds.expired and creds.refresh_token:
#        creds.refresh(Request())
#    else:
#        flow = InstalledAppFlow.from_client_secrets_file(
#            'credentials.json', SCOPES)
#        creds = flow.run_local_server(port=0)
#    with open('token.json', 'w') as token:
#        token.write(creds.to_json())


# The ID and range of the spreadsheet
SAMPLE_SPREADSHEET_ID = '1c8zJleXcZIlb4dULmlUBPtRGvtdzzA4NzZZGoEhNzlI'
SAMPLE_RANGE_NAME = 'People_Profile!A:AG'

# Access the gsheet
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])

# Save as pandas dataframe
df = pd.DataFrame(values)
df.to_csv("./MBGLab-PublicPeopleData.csv", sep=",", index=False, header=False, encoding="utf-8")
