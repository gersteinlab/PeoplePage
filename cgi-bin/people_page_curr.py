#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import func


## start of functions
def html_section_individual(file, section_data):
    for individual in section_data:
        (abbr, first_name, last_name, job_title, website, room, linkedin, comment) = individual

        # Color the icon based on the room
        room2color = {"Bass 426": "#993333", 
                      "Bass 428": "#3ba63c",
                      "Bass 432": "#0F4D92",
                      "Bass 432A": "#0F4D92"}
        if room in room2color.keys():
            svg_color = room2color[room]
        else:
            svg_color = "#4472c0"
        if abbr == "--":
            svg_color = "#cccccc" # all people w/o initial have the same grey color
        if comment.startswith("NoPay"):
          svg_color = "#8c8c8c" # undergrad not getting paid will be dark grey

        # link personal website to name
        if website==" ":
            name_str = """{first_name} {last_name}""".format(first_name=first_name, last_name=last_name)
        else:
            name_str = """<a href="{website}">{first_name} {last_name}</a>""".format(first_name=first_name, last_name=last_name, website=website)

        if linkedin==" ":
            linkedin_str = ""
        else:
            linkedin_str = """
            <a href="{linkedin}">
              <svg width="19px" height="19px">
                <rect width="18px" height="18px" rx="4" fill="#0077b5"/>
                <text x="9px" y="10px" font-weight="bold">in</text>
              </svg>
            </a>""".format(linkedin=linkedin)

        # html output
        file.write("""
              <tr>
                <td width="5px"></td>
                <td width="45px"> 
                  <a href="https://www.ncbi.nlm.nih.gov/pubmed?cmd=PureSearch&dispmax=200&relpubdate=No%20Limit&term=%28%28Gerstein%20Mark%5BAuthor%5D%20NOT%20%281957%5Bdp%5D%20%3A%201990%5Bdp%5D%29%29%29%20AND%20{last_name}%20{first_name}">
                    <svg height="35px" width="35px">
                      <circle cx="17.5px" cy="17.5px" r="17" fill="{svg_color}"/>
                      <text x="17.5px" y="18px">{abbr}</text>
                      Inline SVG Error, plz change web broswer.
                    </svg>
                  </a>
                </td>
                <td width="23px">{linkedin_str}</td>
                <td valign="middle"><p style="font-size:18px; font-family:arial;"><b>{name_str}</b></p></td>
                <td valign="middle"><p style="font-size:18px; font-family:arial;display: inline;">{job_title}</p></td>
              </tr>""".format(first_name=first_name, last_name=last_name, abbr=abbr, svg_color=svg_color, name_str=name_str, job_title=job_title, linkedin_str=linkedin_str))
    return


def html_section_individual_affiliate(file, section_data):
    for individual in section_data:
        (abbr, first_name, last_name, institution, position, website, linkedin) = individual

        # same color for all affiliate
        svg_color = "#58B2DC"

        # link personal website to name
        if website==" ":
            name_str = """{first_name} {last_name}""".format(first_name=first_name, last_name=last_name)
        else:
            name_str = """<a href="{website}">{first_name} {last_name}</a>""".format(first_name=first_name, last_name=last_name, website=website)

        if linkedin==" ":
            linkedin_str = ""
        else:
            linkedin_str = """
            <a href="{linkedin}">
              <svg width="19px" height="19px">
                <rect width="18px" height="18px" rx="4" fill="#0077b5"/>
                <text x="9px" y="10px" font-weight="bold">in</text>
              </svg>
            </a>""".format(linkedin=linkedin)
        if position == " " and institution == " ":
            job_str = ""
        else:
            job_str = position+" @ "+institution

        # html output
        file.write("""
              <tr>
                <td width="5px"></td>
                <td width="45px">
                  <a href="https://www.ncbi.nlm.nih.gov/pubmed?cmd=PureSearch&dispmax=200&relpubdate=No%20Limit&term=%28%28Gerstein%20Mark%5BAuthor%5D%20NOT%20%281957%5Bdp%5D%20%3A%201990%5Bdp%5D%29%29%29%20AND%20{last_name}%20{first_name}">
                    <svg height="35px" width="35px">
                      <circle cx="17.5px" cy="17.5px" r="17" fill="{svg_color}"/>
                      <text x="17.5px" y="17.5px">{abbr}</text>
                      Inline SVG Error, plz change web broswer.
                    </svg>
                  </a>
                </td>
                <td width="23px">{linkedin_str}</td>
                <td valign="middle"><p style="font-size:18px; font-family:arial;"><b>{name_str}</b></p></td>
                <td valign="middle"><p style="font-size:18px; font-family:arial;display: inline;">{job_str}</p></td>
              </tr>""".format(first_name=first_name, last_name=last_name, abbr=abbr, svg_color=svg_color, name_str=name_str, job_str=job_str, linkedin_str=linkedin_str))
    return
## end of functions


## read data
df = pd.read_csv("/var/www/cgi-bin/people/MBGLab-PublicPeopleData.csv", sep=",")

## output html file
f = open("/var/www/www/people/index.html", "w")
func.html_start(f, "index")

## Current Members sections
categories = [
    'pi',
    'staff',
    'research scientist',
    'postdoc',
    'grad',
    'postgrad',
    'undergrad',
    'misc']

categories_title = [
    'Principal Investigator',
    'Laboratory Staff',
    'Research Scientists',
    'Postdoctoral Associates and Fellows',
    'Graduate Students',
    'Full-time Postgrads',
    'Yale Undergrad Students',
    'Misc']

info_col = [
    'abbrev',
    'FirstName',
    'LastName',
    'JobTitle',
    'Website',
    'RoomNumber',
    'Linkedin',
    'Comment']

for category, category_title in zip(categories, categories_title):  
    section_data = func.get_section_data(df, 'Curr', category, info_col)
    func.html_section_start(f, category_title)
    html_section_individual(f, section_data)
    func.html_section_end(f)

## Affiliate members section
info_col = [
    'abbrev',
    'FirstName',
    'LastName',
    'PostLabInstitution',
    'PostLabPosition',
    'Website',
    'Linkedin']

## section data
df = df[df['Affiliate'] == 'YES']
df = df.loc[:,info_col].sort_values(["FirstName","LastName"]).copy().reset_index(drop=True)
df[df.isnull()] = " "
section_data = np.array(df)

func.html_section_start(f, 'Affiliated Members (SI not at Yale)')
html_section_individual_affiliate(f, section_data)
func.html_section_end(f)

## Alumni link
f.write("""
<table class="member-type">
  <tbody>
    <tr>
      <td><font size="+2" face="Arial,Helvetica,Sans-serif"><b><i><a href="http://www.gersteinlab.org/people/alumni.html">Lab Alumni/ae information can be found here</a></i></b></font></td>
    </tr>
  </tbody>
</table>
""")

func.html_end(f)
f.close()
