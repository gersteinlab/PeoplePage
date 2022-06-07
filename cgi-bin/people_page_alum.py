#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import pandas as pd
import func

## start of functions
def html_section_individual(file, section_data, current_mentors):
    for individual in section_data:
        (abbr, first_name, last_name, mentored_by, institution, position, website, netid, start_date, end_date) = individual
        
        svg_color = "#4472c0"

        # link personal website to name
        if website==" ":
            name_str = """{first_name} {last_name}""".format(first_name=first_name, last_name=last_name)
        else:
            name_str = """<a href="{website}">{first_name} {last_name}</a>""".format(first_name=first_name, last_name=last_name, website=website)

        # mark unknown date
        if start_date == " ":
            start_date = "?"
        if end_date == " ":
            end_date = "?"
        
        # get mentors, and check if any are still current members
        if not mentored_by == " ":
            mentors = mentored_by.replace(" ", "").replace("ars+", "").split(",")
            #mentored_by = "Mentored by: " + mentored_by

            if any([m in current_mentors for m in mentors]):
                    svg_color = "#75bee6"
            
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
                <td><font size="+1" face="Arial,Helvetica,Sans-serif"><b>{name_str}</b></font></td>
                <td> <font size="+0" face="Arial,Helvetica,Sans-serif">{position}</font></td>
                <td> <font size="+0" face="Arial,Helvetica,Sans-serif">{institution}</font></td>
                <td> <font size="+0" face="Arial,Helvetica,Sans-serif">{start_date} - {end_date}</font></td>
                <td> <font size="+0" face="Arial,Helvetica,Sans-serif">{netid}</font></td>
                <td> <font size="+0" face="Arial,Helvetica,Sans-serif">{mentored_by}</font></td>
              </tr>""".format(abbr=abbr, svg_color=svg_color, name_str=name_str, position=position, institution=institution, start_date=start_date, end_date=end_date, netid=netid,  mentored_by=mentored_by))
    return
## end of functions


## read data
df = pd.read_csv("/var/www/cgi-bin/people/MBGLab-PublicPeopleData.csv", sep=",")

## output html file
f = open("/var/www/www/people/alumni.html", "w")
func.html_start(f, "alum")

# add header of the main table
col_header = [
    "Current Position",
    "Current Institution",
    "Lab Dates",
    "NetID",
    "Mentor(s)"]
func.html_print_header(f, col_header)

# main table
categories = [
    'staff',
    'research scientist',
    'postdoc',
    'grad',
    'undergrad',
    'misc']

categories_title = [
    'Past Laboratory Staff',
    'Past Research Scientists',
    'Past Postdoctoral Associates and Fellows',
    'Past Graduate Students',
    'Past Undergrad Students',
    'Past Misc']

info_col = [
    'abbrev',
    'FirstName',
    'LastName',
    'MentoredBy',
    'PostLabInstitution',
    'PostLabPosition',
    'Website',
    'NetID',
    'LabStartDate',
    'LabEndDate']

# get list of current people with initials (potential mentors)
current_mentors = df[df["Status"] == "Curr"]["abbrev"].dropna().tolist()

for category, category_title in zip(categories, categories_title):  
    section_data = func.get_section_data(df, 'Alum', category, info_col)
    func.html_section_start(f, category_title)
    html_section_individual(f, section_data, current_mentors)
    func.html_section_end(f)

func.html_end(f)
f.close()
