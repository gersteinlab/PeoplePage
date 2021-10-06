#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import cgi
import cgitb
cgitb.enable()

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("./PeoplePage-005019a507ba.json", scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1c8zJleXcZIlb4dULmlUBPtRGvtdzzA4NzZZGoEhNzlI/edit?hl=en&hl=en#gid=0").get_worksheet(0)

number_people = len(wks.col_values(2))
number_col = len(wks.row_values(1))

all_data = []
for i in range(1,number_col+1):
    curr_col = wks.col_values(i)
    while len(curr_col) < number_people:
        curr_col.append("")
    all_data.append(curr_col)

df = pd.DataFrame(all_data).transpose()
df.columns = df.iloc[0]
df = df.reindex(df.index.drop(0))

df.to_csv("/var/www/cgi-bin/people/MBGLab-PublicPeopleData.csv", sep=",", index=False, encoding="utf-8")