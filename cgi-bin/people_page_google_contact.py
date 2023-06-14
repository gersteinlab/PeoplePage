#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
"""
This script generate csv file in the google contact format
"""

import pandas as pd
import func
import datetime


## ---- start of functions ----
def get_google_contact_flat_file(section_data, f, state):
    """
    section_data: np.array of the google sheet data
    f: file object of the output file
    state: Curr or Alum
    """
    for i in range(len(section_data)):

        # use the first email as the personal email in google contact
        emails = section_data[i,4].split(";")
        emails_personal_str = "* Personal,%s," % (emails[0])
        # if more than one email, add those as other emails
        if len(emails) == 1:
            emails_other_str = "Other,"
        else:
            emails_other = emails[1:]
            emails_other_str = " ::: ".join(emails_other)
            emails_other_str = "Other," + emails_other_str
        emails_str = emails_personal_str + emails_other_str

        # use the first phone as the main+personal email in google contact
        phones = section_data[i,2].split(";")
        phones_personal_str = "* Personal,%s," % (phones[0])
        # if more than one phone number, add those as other phone numbers
        if len(phones) == 1:
            phones_other_str = "Other,"
        else:
            phones_other = phones[1:]
            phones_other_str = " ::: ".join(phones_other)
            phones_other_str = "Other," + phones_other_str
        phones_str = phones_personal_str + phones_other_str


        f.write("%s %s,%s,,%s,%s,,,,,,,%s,,,,,,,,,,,,,,timestamp:%s; type:%s; Initials:%s,,Work,%s,%s,%s\n" \
                % ( 
                    section_data[i,0], section_data[i,1], # name
                    section_data[i,0], # given name
                    section_data[i,1], # family name
                    section_data[i,6], # Yomi Name, using initial
                    section_data[i,5], # Nickname, using skype
                    datetime.datetime.now().strftime("%Y%m%d%H%M%S"), # using current time as timestamp
                    state, # Curr or Alum
                    section_data[i,6], # initial
                    section_data[i,3], # work email, using Yale email
                    emails_str, # other email
                    phones_str)) # phone
    return
## ---- end of functions ----


## read data
df = pd.read_csv("/var/www/cgi-bin/people/MBGLab-PublicPeopleData.csv", sep=",")

categories = [
    'pi',
    'staff',
    'research scientist',
    'postdoc',
    'grad',
    'postgrad',
    'undergrad',
    'misc']

info_col = [
    'FirstName',
    'LastName',
    'PublicCellNumber',
    'YaleEmail',
    'PublicAltEmail',
    'SkypeID',
    'abbrev']

## Curr
f = open("/var/www/www/people/files/people_out_curr.csv", "w")
# header
f.write("Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value,E-mail 2 - Type,E-mail 2 - Value,E-mail 3 - Type,E-mail 3 - Value,Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value\n")
# data
for category in categories:
    section_data_df = pd.DataFrame(func.get_section_data(df, 'Curr', category, info_col))
    section_data = section_data_df[section_data_df[6]!="--"].values # remove people without initial 
    get_google_contact_flat_file(section_data, f, "Curr")
f.close()

## Curr without initial
f = open("/var/www/www/people/files/people_out_undergrad_misc.csv", "w")
# header
f.write("Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value,E-mail 2 - Type,E-mail 2 - Value,E-mail 3 - Type,E-mail 3 - Value,Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value\n")
# data
for category in ['undergrad', 'misc']:
    section_data_df = pd.DataFrame(func.get_section_data(df, 'Curr', category, info_col))
    section_data = section_data_df[section_data_df[6]=="--"].values # only people without initial
    get_google_contact_flat_file(section_data, f, "Curr")
f.close()

## Alum
f = open("/var/www/www/people/files/people_out_alum.csv", "w")
# header
f.write("Name,Given Name,Additional Name,Family Name,Yomi Name,Given Name Yomi,Additional Name Yomi,Family Name Yomi,Name Prefix,Name Suffix,Initials,Nickname,Short Name,Maiden Name,Birthday,Gender,Location,Billing Information,Directory Server,Mileage,Occupation,Hobby,Sensitivity,Priority,Subject,Notes,Group Membership,E-mail 1 - Type,E-mail 1 - Value,E-mail 2 - Type,E-mail 2 - Value,E-mail 3 - Type,E-mail 3 - Value,Phone 1 - Type,Phone 1 - Value,Phone 2 - Type,Phone 2 - Value\n")
# data
for category in categories:
    section_data = func.get_section_data(df, 'Alum', category, info_col)
    get_google_contact_flat_file(section_data, f, "Alum")
f.close()
