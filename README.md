OSCAR-F
=======

Python OSINT Platform

OSCAR-F is designed to aid in the process of information gathering. It was formed with the idea of not having to open
so many tabs in a browser.

There are a few bugs in OSCAR-F, however, we are slowly working on crushing them and working on features.

OSCAR uses a few libraries. These include:
-Twitter
-tweepy
-feedparser
-shodan
-readline

**Please note that you will need to setup ONE twitter app for you/your business.**

**You will probably need to use sudo to run the setup script. This is becasue it creates files and directories.**

The the readline feature is completely optional.

Please be sure to run the DEPENDENCY_CHECK script first!

After running the dependency check, run the setup.py script. This will allow you to setup all necessary auth files/data.

**To scrape pastebin**
To scrape pastebin, enter the regex string to search. Then, run oscar and run the pastebin scraper!

Add regex strings to pSearch.dat located in the root directory. This will be changed soon. 

**To edit rss filter options**
Edit the keywords in /rss/filter.dat

**To add/remove rss feeds**
Edit rss links in /rss/feeds.dat
