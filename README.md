# Table of Contents
1. [About the project](#about-the-project)
    1. [The problem](#the-problem)
    2. [The solution](#the-solution)
    3. [Built with](#built-with)
2. [Getting Started](#getting-started)
    1. [Prerequisites](#prerequisites)
    2. [Running the program](#installation-running-the-program)
        1. [Before running the program (first time only)](#before-running-the-program-first-time-only)
        2. [Running the Python script](#running-the-python-script)
3. [Oddities/Side notes](#odditiesside-notes)
    1. [Using strings instead of ints for booleans in SQLite db](#using-strings-instead-of-ints-for-booleans-in-sqlite-db)
    2. [Additional documentation for webscraper.db](#additional-documentation-for-webscraperdb)
4. [Roadmap](#roadmap)
5. [License](#license)




# About the project

## The problems

1. A couple of years ago, I was tasked with manually checking all pages in a public Confluence space, for images that were missing alternate text.  And if I found images missing alternate text, then I had to add this text to those images.  This task is very cumbersome and tedius.

1. As a budding software engineer, I need to complete real-world side projects.  I was struggling to find real-world coding projects that interested me and were within my level of expertise.  I've never completed real-world coding projects on my own before (I've only completed small coding challenges on websites like [CodeWars](https://www.codewars.com/)).  I like coding when I know I'm working to actually solve a problem I'm having, or a problem someone else is having.   

## The solution

Around April 2022, I got lucky and [watched a YouTuber explain what a webscraper is](https://www.youtube.com/watch?v=Gf1QaBReA2I&t=81s).  I had never heard of webscraping before, and after watching this video, I knew exactly what my first real-world coding project would be.

This CLI program does the following:

1. Scrapes and identifies public Confluence pages belonging to my organization that have images with missing alternate text.
1. Composes individualized messages to send to the Confluence authors who've recently updated these public pages.
    - This program will not email those I consider VIPs (members of my department, and a few other members from other departments).  This program will reassign those pages to me (or whoever the Confluence Coordinators are). 
    - If a public page hasn't been recently updated by an active Confluence author, then this program will reassign those pages to me too (or whoever the Confluence Coordinators are).
1. Emails these individualized messages from a departmental Google account to those Confluence authors, asking them to update their pages.
1. Tracks how long pages have had images with missing alternate text, and reasigns those pages to me (or whoever the Confluence Coordinators are) if those pages have been missing alternate text for 30 days.

This is the third iteration of this project.

## Built with

- [VMware Workstation Player](https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html)
- [Debian](https://www.debian.org/distrib/netinst)
- [Python](https://www.python.org/downloads/)
    - [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/getting_started/)
    - [pip](https://docs.python.org/3/installing/index.html)
- [SQLite](https://www.sqlite.org/index.html)
    - [SQLiteStudio](https://sqlitestudio.pl/) (not required, but recommended)
- [Bob Swift's Atlassian Command Line Interface](https://bobswift.atlassian.net/wiki/x/FQAe)

# Getting Started

## Prerequisites

- OS -- Debian 11 (which was installed on a VM using VMWare Player 17).
    - This Python script should theoretically work on Windows and Mac too, though I haven't tested that yet.
- Python version -- 3.9.2
- SQLite version -- 3.35.4 
- SQL manager -- SQLiteStudio (v3.3.3)
- pip3 packages
    - Selenium WebDriver -- 4.5.0
- Gmail accounts
    - This script assumes that the Confluence Coordinator who runs this script has access to a Google Sheet that lists VIPs who should not be notified about their pages missing alternate text.
    - This script also sends out customized messages to Confluence authors.  This script sends out these messages via a departmental Gmail account, uses smtp.gmail.com to send the message, sends the message via TLS/SSL, and uses [an app password](https://support.google.com/accounts/answer/185833?hl=en) to log in to that Gmail account.

## Running the program

### Before running the program (first time only)

- Update the constants in the [/src/sensitive/emailTemplate.py](https://github.com/ajrworkprojects/webScraperConfluenceAltText_v1.3_prod/blob/master/src/sensitive/emailTemplate.py) and [/src/sensitive/keyInfo.py](https://github.com/ajrworkprojects/webScraperConfluenceAltText_v1.3_prod/blob/master/src/sensitive/keyInfo.py) files.
    - The values for these constants are currently default values.  They must be changed to fit your specifications, or else this script may crash.
- Update the [/src/sensitive/headerLogo.png](https://github.com/ajrworkprojects/webScraperConfluenceAltText_v1.3_prod/blob/master/src/sensitive/headerLogo.png) and [/src/sensitive/footerLogo.png](https://github.com/ajrworkprojects/webScraperConfluenceAltText_v1.3_prod/blob/master/src/sensitive/footerLogo.png) images.  The names of the images need to stay the same, so that they get included in the individualized messages that this script sends to the Confluence authors.
- Search [/src/run.py](https://github.com/ajrworkprojects/webScraperConfluenceAltText_v1.3_prod/blob/master/src/run.py) for "FIXME", and change the argument on that line, from 'credsConfCoord.emailAddr' to 'authorAddr'.
    - This script initially sends all emails to the Confluence Coordinator who runs this script.  This way the Coordinator could review the emails if they want to (which is encouraged).
    - Changing this argument will email the individualized messages to their respective Confluence authors.

### Running the Python script

Run the [/src/run.py](https://github.com/ajrworkprojects/webScraperConfluenceAltText_v1.3_prod/blob/master/src/run.py) file.  

The script will eventually prompt you to provide two sets of credentials.  The script will also provide updates as this script runs. 

# Oddities/Side notes

### Using strings instead of ints for booleans in SQLite db

SQLite's official [Datatypes In SQLite](https://www.sqlite.org/datatype3.html) documentation says,

> SQLite does not have a separate Boolean storage class. Instead, Boolean values are stored as integers 0 (false) and 1 (true).

0's and 1's may be more difficult for engineers to read, when they review this codebase.  So I use the strings "FALSE" and "TRUE" instead.

### Additional documentation for webscraper.db

- [Tables, columns, and their purposes](https://docs.google.com/spreadsheets/d/1T-vxVd8HH2ZWxJhPuKN-l00aifjpW1kcJpCSu3-55Ss/edit#gid=0)
- [ER diagram for webscraper.db](https://drive.google.com/file/d/1gMjRWo2lrrMB8t8xviobIL-K0ViUEV2A/view)

# Roadmap

### Version 1.4 and beyond

- [ ] Create a new VMWare VM that runs a stripped down verison of Debian and only has the necessary programs installed for this script to run (doing this may reduce the attack surface of this script).

- [ ] Look into a way to use Docker to ship this script to other computers with different OSes.

- [ ] Add feature to Python script, so that the user can choose via the CLI to have drafts of the messages sent to a subdirectory.

- [ ] Look into using [keyring](https://pypi.org/project/keyring/) to store the credentials that the Confluence Coordinator passes to this script.

### Version 1.3 (current)

- [x] Ensure that the script sanitizes all data it inserts into the db, by checking that incoming data to ensure it only matches predefined data (the script likely already does this, but it doesn't hurt to doublecheck).

- [x] Remove the beautifulsoup4 module from this script.

  - [x] Incorporate acli.
  
  - [x] Incorporate Selenium WebDriver.

- [x] Reorganize methods by imported modules, instead of by when those methods are called in the script.

- [x] Pass variable names along with variable values, when I pass values to methods.  Doing this should make it easier for beginning engineers to understand.

- [x] Search [Synk Advisor](https://snyk.io/advisor/python) for all the Python packages this script uses, to ensure they all receive a high health score (I have noticed that other packages were getting automatically added to this script when I ran it).

- [x] <span style="color:IndianRed">~~Automatically upload messages.csv file to the associated Google Sheet.  (Optionally) Automatically email Confluence authors when the script uploads the messages.csv file to the the Google Sheet~~</span> The script no longer requires the user to upload the custom messges to a Google Sheet.  The script automatically emails the authors using the smtplib, ssl, and some MIME Python libraries

- [x] <span style="color:IndianRed">~~Add stops so that the Python script reminds the user to check the list of VIPs, before continuing to run the program.~~</span>  No longer necessary, since the script now automatically checks for these VIPs before creating and emailing the custom messages

- [x] Check all variable names, to ensure they're accurate and clear.

- [x] For variables that store one-item tuples, either change those variables so that they store the actual values, or add **_t** to the end of the variable names.

- [x] Add checks into the Python script, that ensures that one feature doesn't run before another feature runs.

- [x] Update the Python script so that it checks to see if the webscraper.db exists.  If the db exists, then the Python script should continue running.  If it doesn't, then the script should create the db.

- [x] <span style="color:IndianRed">~~Update Python script, so that it checks to see if the Python script has been run once already.  Store that boolean in the db.~~</span>  No longer necessary, because 1) this script uses Bob Swift's Atlassian Command Line Interface, and 2) the overall logic of the codebase is more efficient.

- [x] <span style="color:IndianRed">~~Figure out how the Python script can get updated cookie values, while the Python script is running (as of now, the program quits when the Python script can't validate the cookies).~~</span> No longer necessary, since this script uses Selenium WebDriver instead of the request library and the BeautifulSoup pip package.

- [x] <span style="color:IndianRed">~~Figure out to update the Python script, so that users don't have to manually choose which major feature to run.  The user should just run the script, and the script should be able run all major features on its own.  The script should also be able to determine where to begin, if the script stops running because the Internet was blocked or the computer is turned off.~~</span>  No longer necessary, because the overall logic of the codebase is more efficient.

### Version 1.2

- [x] Update all PKB pages that are assigned to me to update.

- [x] Fix broken "image is embedded from an external website" links.

- [x] Update CONFLUENCE_LINKS table.  That table should have just one column for date, and another column (called "wasPageRecentlyUpdated") that stores a boolean for if the date I just found matches the date currently in the table.  If the dates match, then "FALSE"; if the dates don't match, then "TRUE" and update the date in the table.  Also change the logic in the Python script that checks for TRUE values, instead of comparing dates.

- [x] Review db documentation and ensure it matches the actual db.

- [X] Build confirmation messages throughout the CLI app.

# License

Copyright (C) 2022 ajrworkprojects

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
