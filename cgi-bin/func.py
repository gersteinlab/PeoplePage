#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd

def html_start(file, page_type):
    """
    Writing the start part of html codes to the file
    including <html>, <head>, start of the <body>, whole <div id="global-title-container">, start of <div id="page"> and <div id="main-{page_type}"> 

    Parameter:
        file: output file object
        page_type: choice of ["index", "info", "alum"]
    """

    file.write('''<!DOCTYPE html>
<html>
<head>
  <title>Gerstein Bioinformatics Group Members</title>
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
  <link rel="stylesheet" href="http://www.gersteinlab.org/media/css/style.css?v=1" />
  <script language="JavaScript" src="http://www.gersteinlab.org/media/js/modernizr-1.5.min.js"></script>
  <link rel="stylesheet" type="text/css" href="styles/index.css?v=1" />
  <style type="text/css" media="print">
    @page {{
      size: auto;
      margin: 2;
    }}
  </style>
</head>
 
<body> 
  <div id="global-title-container"> 
    <div id="title-wrapper" class="clearfix"> 
      <div id="title-left"> 
        <a href="http://www.gersteinlab.org"> <strong>Gerstein</strong>Lab</a>
      </div> 
      <div id="title-right"> 
        <a href="http://cbb.yale.edu">Bioinformatics</a>
      </div> 
    </div> 
  </div>
  
  <div id="page">
    <div id="main-{page_type}"> 
      <div id="menu">
        <br/> 
        <a href="http://www.gersteinlab.org/people/" style="font-size:18px;">Current Members</a>
        <a href="http://www.gersteinlab.org/people/curr_info.html" style="font-size:18px;">(Info)</a>&nbsp;•&nbsp;
        <a href="http://www.gersteinlab.org/people/alumni.html" style="font-size:18px;">Alumni/ae</a>&nbsp;•&nbsp;
        <a href="http://info.gersteinlab.org/Additional_Information_about_Personnel" style="font-size:18px;">Wiki</a>
        <br/> 
        <br/> 
        <br/> 
        <br/>
      </div>
'''.format(page_type=page_type))
    return


def html_end(file):
    """
    Writing the end part of html codes to the file
    including </div id="main-{page_type}">, </div id="page">, </body>, </html>

    Parameter:
        file: output file object
    """
    file.write('''
    </div> 
  </div>  
</body>
</html> 
''')
    return


def html_print_header(file, header):
    """
    Print header of the main section table

    Parameter:
        file:
        header: list of str, names of the columns
    """

    # header string
    header_str = ["""<td><font size="+0" face="Arial,Helvetica,Sans-serif"><b>{i}</b></font></td>""".format(i=i) for i in header]
    header_str = "\n".join(header_str)

    # html output
    file.write("""
      <table class="member-header"> 
        <tbody> 
          <tr>
            <td width="5px"></td>
            <td width="45px"></td>
            <td></td>
            {header_str}
          </tr>
        </tbody> 
      </table> 
      <div class="sep-br"> 
          <br/> 
          <br/>
      </div>
""".format(header_str=header_str))
    return
  

def get_section_data(full_df, status, category, col):
    """
    Get the data from full sheet and filter as needed.
    Return as numpy array. Order of the columns is the same as col parameter.
    Notice any empty data will be replaced by " " (length ONE space)

    Parameter:
        full_df: df object of the full google sheet
        status: str, value of Status column
        category: str, value of Category column
        col: list of str, names of the columns in the google sheet that will be kept
    """

    df = full_df.query("Status == '%s' & Category == '%s'" % (status, category))

    df = df.loc[:,col].sort_values(["FirstName","LastName"]).copy().reset_index(drop=True)
    df[df.isnull()] = " "
    df = np.array(df)
    return df


def html_section_start(file, section_title):
    """
    Writing the start part of one section,
    including the section title and the start of <table> and <tbody>

    Parameter:
        f: file
        section_title: str
        section_data: np.array object, each row is an individual
        html_print_individual_func: the function to use to print the html, see following functions for details
    """

    file.write("""
      <table class="member-type"> 
        <tbody> 
          <tr> 
            <td><font size="+2" face="Arial,Helvetica,Sans-serif"><b><i>{section_title}</i></b></font></td> 
          </tr> 
        </tbody> 
      </table> 
      <table class="member-data"> 
        <tbody>""".format(section_title=section_title))
    return


def html_section_end(file):
    """
    Writing the end part of one section,
    including </tbody> and </table>
    """
    file.write("""    
        </tbody> 
      </table> 
      <div class="sep-br"> 
        <br/> 
        <br/>
      </div>""")
    return
