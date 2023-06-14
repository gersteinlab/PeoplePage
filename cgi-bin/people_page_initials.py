#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import pandas as pd
import func
from datetime import date

## read data
df = pd.read_csv("/var/www/cgi-bin/people/MBGLab-PublicPeopleData.csv", sep=",")

## output html file
f = open("/var/www/www/people/initial.html", "w")

######## initial.html ########
info_col = [
    'FirstName',
    'LastName',
    'abbrev']

categories = [
    'pi',
    'staff',
    'research scientist',
    'postdoc',
    'grad',
    'postgrad',
    'undergrad',
    'misc']

# print update date
f.write("""<html>
<head>
  <title>Gerstein Bioinformatics Group Members</title>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
</head>

<body>
<p style="margin-left: 20px;">Last auto update: {daynow}</p>
<br />
<div style="margin-left: 20px;">""".format(daynow=date.today().strftime("%Y-%m-%d")))

# find abbreviation not equal to "--"
for category in categories:
    section_data = func.get_section_data(df, 'Curr', category, info_col)
    abbrevs = pd.DataFrame(section_data)[2].values
    for abb in abbrevs:
        if abb != "--":
            f.write(abb+'<br />')

f.write("""</div>
</body>
</html>""")
f.close()