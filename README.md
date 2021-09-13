# FlatHunter

![FlatHunter](/assets/web_ui.png)

## Introduction

FlatHunter is a simple tool designed to lessen the tedium of searching for a new flat (or apartment in US English). It will (responsibly) scrape Rightmove (a UK real estate website) accordingly to chosen criteria and email out a regular PDF digest of new flats.
<p align="center">
  <img width="300" height="auto" src="/assets/example_email.jpg">
 </p>


## Design / usage

'application.py' defines a Flask webapp which acts as the GUI for the tool by accepting user input, calling scraping functions from 'helpers.py', and returning results to the user. Upon performing a search, the user's desired attributes are used to generate the target URL via a call to URL_generator(). Next application.py will make a call to either hunt() or scheduled_hunt() as appropriate - the user can either perform a 'Search Now' or 'Regular Search' - to initiate the scraping process.
    
For each http request performed, the returned HTML is parsed using BeautifulSoup and trimmed down to the useful stuff (json data for the properties present on that page) which is then written to a SQLlite database of properties. Further pages of results (if present) are scraped until the scraper identifies that it has reached the end (by interrogating pagination data). Images are also downloaded. To minimise bandwith usage, the pictures are downloaded as thumbnails and are not re-downloaded if the property has already been scraped by FlatHunter.
    
Random waits are introduced between web requests to avoid creating nuisance amounts of traffic. Because of this, a search with more than one page of results can take a while. To avoid apparent hanging, for 'Search Now' progress is displayed on a simple loading screen implemented with some client-side javascript which queries the value of a counter variable in the python backend and redirect the browser to the results when they are ready.

Alternatively, if the user elects to set up a 'Regular Search' scraping will occur in the background. At regular intervals a summary of newly discovered properties will then be appended to a basic PDF (created from the HTML with the xhtml2pdf library) and emailed to the user:


![example pdf](/assets/example_pdf.png)

 

## Email config

*This should only be done on an account set up and used exclusively for this service*

In order to send emails the script must have access to a gmail account with ['allow less secure apps'](https://myaccount.google.com/lesssecureapps). Credentials are imported as environment variables - to set this up create a file called .env in the application directory with the following structure:
    
    address=senderemailaddress
    password=password
    recipient=recipientemailaddress

## Other notes

This script was designed as personal tool (and has indeed been useful when I've been looking for somewhere to live) and is therefore currently hard-coded to search in Edinburgh. To search elsewhere you should first perform a search on Rightmove to find the 'locationIdentifier' in the URL, then edit application.py accordingly. It's also possible to add custom search criteria not covered in the web app by editing the base URL in helpers.py.

Future work on this project could be to generalise it to allow further search criteria and locations without requiring code edits.

## Disclaimer

I have written this script as an educational exercise to practise programming, learn about web-scraping, and complete [CS50's final project](https://cs50.harvard.edu/x/2021/project/). I have tried to ensure it is as responsible as possible (see above).
