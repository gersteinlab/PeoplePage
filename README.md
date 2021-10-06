# www.gersteinlab.org/people/

GitHub repository for people page scripts
For more information, please visit lab [private wiki](http://wiki.gersteinlab.org/labinfo/People_Page)

## Directories
All files are hold on www.gersteinlab.org server  
/Folder-In-This-Repo -> /Actual/Location/In/Server
* /cgi-bin -> /var/www/cgi-bin/people/
* /www -> /var/www/www/people/

Credential and main gsheet are replaced by placeholder in this repo.

## Update

To manually rebuild, simply run `http://www.gersteinlab.org/cgi-bin/people/main.py`

## Files explained

* `main.py`: run all the following files
* `gsheet_download.py`: download the master Google spreadsheet as a CSV file
* `people_page_curr.py`: index page
* `people_page_curr_info.py`: curr_info.html page
* `people_page_alum.py`: alumni.html page
* `people_page_google_contact.py`: generate the two Google contact compatible csv files (could be found in wiki)
* `people_page_initials.py`: initial.html page
* `func.py`: helper functions for printing the html template
