# -*- encoding: utf-8 -*-
from lxml import html  
import csv,os,json,io
import requests
from exceptions import ValueError
from time import sleep
import urllib,urllib2, os, sys
from random import randint
import time
import codecs
import pickle
import csv

    
def writeToCSV(database):
    
    keywordlist = []
    for i in range (0, len(database)):
      for a in range (0, len(database[i]["KEYWORDS"])):
        if database[i]["KEYWORDS"][a] not in keywordlist:
          keywordlist.append(database[i]["KEYWORDS"][a])

    
    headers = ["title","pages","author","reviews","rating","ku","price","blurb","url"]
    for j in range(0, len(keywordlist)):
        headers.append(keywordlist[j])
    headers.append("category")
    headers.append("rank")
    headers.append("category")
    headers.append("rank")
    headers.append("category")
    headers.append("rank")      
        
    filename = title + ".csv"
    b = open(filename, 'wb')
    a = csv.writer(b)
    a.writerows([headers])   
    for i in range(0, len(database)):
                entry = []
                entry.append(database[i]["NAME"])
                entry.append(database[i]["PAGES"])
                entry.append(database[i]["AUTHOR"])
                entry.append(database[i]["REZENSIONEN"])
                entry.append(database[i]["RATING"])
                entry.append(database[i]["KU"])
                entry.append(database[i]["PRICE"])
                entry.append(database[i]["BLURB"])
                entry.append(database[i]["URL"])
                for j in range(0, len(keywordlist)):
                    if keywordlist[j] in database[i]["KEYWORDS"]:
                      entry.append("1")
                    else:
                      entry.append("0")
                if len(database[i]["1CATEGORY"]) > 2 and database[i]["1RANK"]>0:
                  entry.append(database[i]["1CATEGORY"])
                  entry.append(database[i]["1RANK"])
                if len(database[i]["2CATEGORY"]) > 2 and database[i]["2RANK"]>0:
                  entry.append(database[i]["2CATEGORY"])
                  entry.append(database[i]["2RANK"])
                if len(database[i]["3CATEGORY"]) > 2 and database[i]["3RANK"]>0:
                  entry.append(database[i]["3CATEGORY"])
                  entry.append(database[i]["3RANK"])
                
#                for t in range(0, len(tagcloud)):
#                    if tagcloud[t] in database[i]["TAG"]:
#                        entry.append(1)
#                        
#                    else:
#                        entry.append(0)
                      
#                print entry
                a.writerows([entry])
    b.close()
    print "CSV saved."

    
    
if __name__ == "__main__":



  if len(sys.argv) < 2:
      print "You must set a title for your verification. It must be the same as the one used for scraping earlier (the first argument you passed to the scrape.py." 
      sys.exit()
  else:
      title = sys.argv[1]
      
  filename = title+".json"
  try:
    with open(filename, 'rb') as f:
      database = pickle.load(f)
  except:
    print "No database found. Check title (first argument) or scrape data first."
  
  keywordlist = []
  for i in range (0, len(database)):
    for a in range (0, len(database[i]["KEYWORDS"])):
      if database[i]["KEYWORDS"][a] not in keywordlist and database[i]["KEYWORDS"][a] != "bestsellers":
        keywordlist.append(database[i]["KEYWORDS"][a])
  
  k = ""
  while k not in (keywordlist):
    k = raw_input("For which keyword do you want to verify the titles? Options: " + str(keywordlist) + "\n")
 
  print keywordlist
  print "\n"
  titlehints = ""
  titlehints = raw_input("Specify words/word groups that DEFINITELY put a book in the category " + k + ", if they appear in the TITLE. Seperate them by commas. Upper or lower case doesn't matter. You can leave this empty.\n   E.g. for 'krimi', you could use 'Fall,Mord', since a lot of krimi titles contain something like 'Kommisar Clevers 6. Fall', or the word 'Mord'.\n")
 
  print "\n"
  contenthints = ""
  contenthints = raw_input("Specify words/word groups that DEFINITELY put a book in the category " + k + ", if they appear in the CONTENT. Seperate them by commas. Upper or lower case doesn't matter.  You can leave this empty.\n   E.g. for 'Romantik', you could use 'Auf den ersten Blick,Liebe'.\n")
 
  print "\n"
  nogo = ""
  nogo = raw_input("Specify words/word groups that will take the book OUT of the category " + k + ". Seperate them by comma, cases don't matter, can be left empty.\n   E.g. 'Fantasy' if you are researching historicals which should not contain the word Fantasy in their desription.\n") 
  
  print "\n"
  placement = ""
  placement = raw_input("Name a category where the books must have a ranking.\nE.g. 'Erotik > Romane' if you only want books that have a rank in this category.\n")

  


  filename = title+".json"
  with open(filename, 'rb') as f:
      database = pickle.load(f)
  #print len(database)
  
  for i in range(0, len(database)):
      #sanitizing the content a little
      
      database[i]["KEYWORDS"] = list(set(database[i]["KEYWORDS"]))
      
      find = database[i]["BLURB"].lower().find(database[i]["AUTHOR"].lower())
      if find > -1:
          database[i]["BLURB"] = database[i]["BLURB"][:find]
      
      find = database[i]["BLURB"].lower().find("lustvolle lekt".lower())
      if find > -1:            
          database[i]["BLURB"] = database[i]["BLURB"][:find]
      
      find = database[i]["BLURB"].lower().find("Weitere Romane".lower())
      if find > -1:            
          database[i]["BLURB"] = database[i]["BLURB"][:find]
          
      find = database[i]["BLURB"].lower().find("Weitere B".lower())
      if find > -1:            
          database[i]["BLURB"] = database[i]["BLURB"][:find]

          
  for i in range (0, len(database)):
    truestory = False
    #we start with not believing that the element belongs to the keyword k

    thints = []
    chints = []
    nogos = []
    
    if len(titlehints) > 0:
      thints = titlehints.split(",")
      for t in range (0,len(thints)):
        thints[t]=thints[t].strip()
        thints[t]=" " + thints[t]
        thints[t]=thints[t].lower()
    if len(contenthints) > 0:
      chints = contenthints.split(",")
      for t in range (0,len(chints)):
        chints[t]=chints[t].strip()
        chints[t]=" " + chints[t]
        chints[t]=chints[t].lower()
    if len(nogo) > 0:
      nogos = nogo.split(",")
      for t in range (0,len(nogos)):
        nogos[t]=nogos[t].strip()
        nogos[t]=" " + nogos[t]
        nogos[t]=nogos[t].lower()
    
    
    
    for n in range (0, len(thints)):
      if database[i]["NAME"].lower().startswith(thints[n]):
        print database[i]["NAME"] + " has '" + thints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(thints[n] + " ")
      if find > -1:
        print database[i]["NAME"] + " has '" + thints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(thints[n] + ".")
      if find > -1:
        print database[i]["NAME"] + " has '" + thints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(thints[n] + "!")
      if find > -1:
        print database[i]["NAME"] + " has '" + thints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(thints[n] + "?")
      if find > -1:
        print database[i]["NAME"] + " has '" + thints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(thints[n] + ":")
      if find > -1:
        print database[i]["NAME"] + " has '" + thints[n] + " ' and is definitely a " + k + " book."
        
      if database[i]["BLURB"].lower().startswith(chints[n]):
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + chints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(chints[n] + " ")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + chints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(chints[n] + ".")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + chints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(chints[n] + "!")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + chints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(chints[n] + "?")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + chints[n] + " ' and is definitely a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(chints[n] + ":")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + chints[n] + " ' and is definitely a " + k + " book."






  
    
    
    
    ### sort out the nogo-offenders, i.e. all books that have 'no go' words or phrases in their title or content
    for n in range (0, len(nogos)):
      if database[i]["NAME"].lower().startswith(nogos[n]):
        print database[i]["NAME"] + " has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(nogos[n] + " ")
      if find > -1:
        print database[i]["NAME"] + " has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(nogos[n] + ".")
      if find > -1:
        print database[i]["NAME"] + " has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(nogos[n] + "!")
      if find > -1:
        print database[i]["NAME"] + " has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(nogos[n] + "?")
      if find > -1:
        print database[i]["NAME"] + " has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["NAME"].lower().find(nogos[n] + ":")
      if find > -1:
        print database[i]["NAME"] + " has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        
        
      if database[i]["BLURB"].lower().startswith(nogos[n]):
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(nogos[n] + " ")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(nogos[n] + ".")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(nogos[n] + "!")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(nogos[n] + "?")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + nogos[n] + " ' and is definitely not a " + k + " book."
        truestory = False;
      find = database[i]["BLURB"].lower().find(nogos[n] + ":")
      if find > -1:
        print "Description '" + database[i]["BLURB"][find-35:find+35] + "' has '" + nogos[n] + " ' and is definitely not a " + k + " book."


      if len(placement) > 0:
        if (placement.lower() not in database[i]["1CATEGORY"].lower()) and (placement.lower() not in database[i]["2CATEGORY"].lower()) and (placement.lower() not in database[i]["3CATEGORY"].lower()):
          truestory = False;
        

  
  filename = title + "-verified" + ".json"
      
  with open(filename, 'wb') as f:
      print "\nverified database saved (" + filename + ")\n"
      pickle.dump(database, f)

  a = ""
  while a not in (["y","n"]):
    a = raw_input("Do you want to override the loaded database with the verified one that was created? A backup has been made anyway. This will make the changes permanent and save a csv. (y/n)")
  if a == "y":
    filename = title + ".json"
    with open(filename, 'wb') as f:
        print "database saved (" + filename + ")"
        pickle.dump(database, f)
    
    writeToCSV(database)
    
    
    
        
  
