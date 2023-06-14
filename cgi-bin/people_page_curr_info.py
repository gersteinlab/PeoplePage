#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
"""
This script generate the info page for current people
"""

import pandas as pd
import func

## ---- start of functions ----
def html_section_individual(file, section_data):
    for individual in section_data:
        (abbr, first_name, last_name, start_date, netid, ymail, email, phone, era) = individual

        # default icon color
        svg_color = "#4472c0"
        # people w/o initial is grey
        if abbr == "--":
            svg_color = "#dedede"

        # for columns of private information, show indicator
        # tick for having the info, cross for not
        indicator_data = []
        indicator_col = (ymail, email, phone, era)
        for col in indicator_col:
            if col == " ":
                indicator_data.append("""<td><font size="+0" face="Arial,Helvetica,Sans-serif" color="red">✘</font></td>""")
            else:
                indicator_data.append("""<td><font size="+0" face="Arial,Helvetica,Sans-serif" color="F0F0F0">✔</font></td>""")
        indicator_data = "\n".join(indicator_data)

        # html output
        file.write("""
              <tr>
                <td width="5px"></td>
                <td width="45px"> 
                  <svg height="35px" width="35px">
                    <circle cx="17.5px" cy="17.5px" r="17" fill="{svg_color}"/>
                    <text x="17.5px" y="17.5px">{abbr}</text>
                    Inline SVG Error, plz change web broswer.
                  </svg>
                </td>
                <td><font size="+1" face="Arial,Helvetica,Sans-serif"><b>{first_name} {last_name}</b></font></td>
                <td><font size="+0" face="Arial,Helvetica,Sans-serif">{Sdate}</font></td>
                <td><font size="+0" face="Arial,Helvetica,Sans-serif">{netid}</font></td>
                {indicator_data}
              </tr>""".format(abbr=abbr, svg_color=svg_color, first_name=first_name, last_name=last_name, Sdate=start_date, netid=netid, indicator_data=indicator_data))
    return
## ---- end of functions ----


## read data
df = pd.read_csv("/var/www/cgi-bin/people/MBGLab-PublicPeopleData.csv", sep=",")

## output html file
f = open("/var/www/www/people/curr_info.html", "w")
func.html_start(f, "info")

# add header of the main table
col_header = [
    'StartDate',
    'NetID',
    'YaleEmail',
    'AltEmail',
    'Phone',
    'eRA']
func.html_print_header(f, col_header)

# main table
categories = [
    'pi',
    'staff',
    'research scientist',
    'postdoc',
    'grad',
    'postgrad',
    'undergrad']

categories_title = [
    'Principal Investigator',
    'Laboratory Staff',
    'Research Scientists',
    'Postdoctoral Associates and Fellows',
    'Graduate Students',
    'Full-time Postgrads',
    'Undergrad Students']

info_col = [
    'abbrev',
    'FirstName',
    'LastName',
    'LabStartDate',
    'NetID',
    'YaleEmail',
    'PublicAltEmail',
    'PublicCellNumber',
    'eRA account']

for category, category_title in zip(categories, categories_title):  
    section_data = func.get_section_data(df, 'Curr', category, info_col)
    func.html_section_start(f, category_title)
    html_section_individual(f, section_data)
    func.html_section_end(f)

func.html_end(f)
f.close()
