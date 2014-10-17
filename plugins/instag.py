#!/usr/bin/env python

import urllib2

def checker(usernom):
  #use username from FB profile and try it against instagram
  inst = "http://instagram.com/"+usernom
  try:
    data = urllib2.urlopen(inst)
    valid = 1
    #data = data.read()
    #print data
  #If we get a 404/not found, then set valid to 0
  except urllib2.HTTPError:
    valid = 0
  if valid == True:
    print
    print "---------"
    print "Found "+usernom+" on instagram!"
    print "Profile link: http://instagram.com/"+usernom
    print "---------\n"
  elif valid == False:
    return
