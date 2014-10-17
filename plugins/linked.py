#!/usr/bin/env python

from bs4 import BeautifulSoup as bsoup
import requests as req
import mechanize, urllib, urllib2, re, csv, sys, json
import os, time, random, cookielib, thread

def start():
  pos = raw_input("Enter position: ")
  pos = pos.lower()
  com = raw_input("Enter company: ")
  com = com.lower()
  useout = raw_input("Save output? [y/n]: ")
  global saveout
  if useout == "y":
    saveout = True
  else:
    saveout = False
  bing(pos,com,saveout)


def csvwrite(p1,c1,plink):
  saveFile = open('OUTPUT.csv','a')
  saveFile.write(p1+"+"+c1+"+"+plink)
  saveFile.write('\n')
  saveFile.close()


def bing(pos,com,saveout):
  #Setup browser using mechanize.
  br = mechanize.Browser()
  #Accept cookies...we need a cookiejar. :)
  cj = cookielib.LWPCookieJar()
  br.set_cookiejar(cj)
  br.set_handle_equiv(True)
  #br.set_handle_gzip(True)
  br.set_handle_redirect(True)
  br.set_handle_referer(True)
  br.set_handle_robots(False)

  br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

  #user agent. This can always be changed or read from a file later
  br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.1 Safari/537.17')]

  #craft url for bing :D
  burl = 'http://www.bing.com/search?q=site:linkedin.com '+'"'+pos+'"'+" "+'"'+com+'"'

  #replace any spaces in our query with url encoded values
  r = br.open(burl.replace(' ', '%20'))
  #read html
  html = r.read()
  #parse html through beautifulsoup
  soup = bsoup(html)
  #result = soup.find_all('div', {"class" : "sb_tlst"})
  result = soup.find_all('li', {"class" : "b_algo"}) if soup.find_all('li', {"class" : "b_algo"}) else soup.find_all('div', {"class" : "sb_tlst"})
  refs = []
  for i in result:
    link = i.a['href'] #Get Hrefs from bing's source
    #Quick validation to ensure we are actually getting linkedin
    if "/dir/" in link or "groupItem" in link or not "linkedin.com" in link:
      continue
    else:
      refs.append(link)
  #use set to help remove possible duplicate links
  nodupLinks = set(refs) #try and remove duplicates

  #Add the company name to an array. This is for a future idea
  comp = []
  comp.append(com)

  for links in nodupLinks:
    #open a link from the links array.
    r = br.open(links)
    html = r.read()
    soup = bsoup(html) #Have bs4 read the html from linkedin
    #look for the title element within linkedin
    result_name = soup.find("title")
    result_name = result_name.string.strip().split(' | ')
    #Some validation to ensure that we get position info if there is/isn't a headline
    result_title = soup.find('p',{"class" : "headline-title title"}) if soup.find('p',{"class" : "headline-title title"}) else soup.find('ul',{"class" : "current"}) or soup.find('p',{'class' : 'title'})
    try:
      #Validation to ensure that the company name IS a current position...not a past one
      if not comp[0] in result_title.string.lower():
        continue
      else:
        #results of the query
        print
        print "-----------START--------------"
        print result_name[0].encode('utf-8'),result_title.string.encode('utf-8')
        print links
        print "------------END---------------"
        print
        #check for boolean val on saveout.
        if saveout:
          result_title.string = result_title.string.strip('\n')
          restitle = result_title.string.encode('utf-8')
          resnom = result_name[0].encode('utf-8')
          thread.start_new_thread(csvwrite,(resnom,restitle,links))
        #skip the DL process id saveout is set to no/0
        else:
          pass
    except:
      pass
    time.sleep(2) #sleep real quick before crushing linkedin with requests
  refs = [] #clear temporary array after running
  comp = [] #clear temporary array after running
  return

#function to try and remove duplicates from the lists. 
def dupr(saveout):
  #with open('OUTPUT.csv','r') as f1, open('LINKEDIN_OUT.csv','a') as f2:
  f1=csv.reader(open('OUTPUT.csv', 'r'), delimiter='+')
  f2=csv.writer(open('LINKEDIN_OUT.csv', 'w'), delimiter='+')
  #seen = set()
  links = set()
  for row in f1:
    if row[2] not in links:
      f2.writerow(row)
      links.add( row[2] )
  return
