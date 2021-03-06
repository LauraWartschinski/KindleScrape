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

keywords = []
keycloud = []
hindex = 0
last = 0
pagedepth = 0
title = ""


################### CLEAN HTML (HELPER) ############################
def clean_html(content):
    content = content.replace("</p>"," ")
    content = content.replace("<p>"," ")
    content = content.replace("<strong>","")
    content = content.replace("</strong>","")
    content = content.replace("<br>"," ")
    content = content.replace("<br />"," ")
    content = content.replace("<em>","")
    content = content.replace("</em>","")
    content = content.replace("<b>","")
    content = content.replace("</b>","")
    content = content.replace("<div>"," ")
    content = content.replace("</div>","")
    content = content.replace("<h1>"," ")
    content = content.replace("</h1>","")
    content = content.replace("<h2>"," ")
    content = content.replace("</h2>","")
    content = content.replace("<h3>"," ")
    content = content.replace("</h3>","")
    content = content.replace("\n"," ")
    content = content.replace("\t","")
    content = content.replace("   "," ")
    content = content.replace("  "," ")
    
    
    while "<" in content:
        start = content.index("<")+1
        if ">" in content:
            stop = content.index(">")
            if (stop < start):
                badstring = content[:start-1]
                badstring = badstring.replace(">","")
                content = badstring + content[start:]
            else:
                between = content[start:stop]
                if "<" in between or ">" in between:                
                    between.replace("<","")
                    between.replace(">","")
                    content = content[:start-1] + between + content[stop+1:]
                else:
                    pre = content[:start-1]
                    post = content[stop+2:]
                    content = pre + post
        else: 
            break
    
    content = content.replace("<","")
    content = content.replace(">","")
    
    
    if content.startswith(" "):
      return content[1:]
    
    return content




################### COLLECT LINKS FOR KEYWORD (pagedepth PAGES) ############################


def collectLinksForKeyword(key):
    global pagedepth
    filename = key + ".json" + "DISABLED"
    
    filenameold = "new_" + key + ".json" + "DISABLED"
    if os.path.isfile(filenameold):
        print "we already have fetched all the asins for that keyword!"
        with open(filenameold) as data_file:    
            data = json.load(data_file)
            #print data
            return list(set(data))

    if os.path.isfile(filename):
        print "we already have fetched all the asins for that keyword!"
        with open(filename) as data_file:    
            data = json.load(data_file)
            #print data
            return list(set(data))
    else:
      extracted_data = []
      for i in range(0,pagedepth):
  
  
	b = "3D530886031"
	if cat == "krimi/thriller":
		b = "3D5870279031"        
	if cat == "gegenwart":
		b = "3D610653031"        
	if cat == "fantasy/scifi":
		b = "3D567119031"        
	if cat == "liebe":
		b = "3D610659031"        
	if cat == "erotik":
		b = "3D611339031"        
	if cat == "historisch":
		b = "3D610655031"        
	if cat == "ratgeber":
		b = "3D567131031"        
	if cat == "politik/geschichte":
		b = "3D567130031"    
	if cat == "jugendbuch":
		b = "3D4931127031"        
	if cat == "fachbuch":
		b = "3D567118031"

	url = "https://www.amazon.de/s/&url=node%" + b + "&field-keywords="  + key + "?page=" + str(i)

	url = "https://www.amazon.de/s/url=search-alias%3Ddigital-text&field-keywords=" + key + "?page=" + str(i)
#	url = "https://www.amazon.de/s/&url=node%3D611339031&field-keywords=" + key + "?page=" + str(i) //Erotik
	new = AmazonParserLinks(url)
	if (len(new)) > 0:
	  extracted_data = extracted_data + new
	else:
	  break
      print "Found " + str(len(extracted_data)) + " links for '" + key + "'."
      save(extracted_data,key)
      
    return list(set(extracted_data))
  


################### COLLECT LINKS FOR BESTSELLERS ############################

def collectLinks():
    extracted_data = []
    
    b = "530886031"    
    if cat == "krimi/thriller":
        b = "567126031"        
    if cat == "gegenwart":
        b = "610653031"        
    if cat == "fantasy/scifi":
        b = "567119031"        
    if cat == "liebe":
        b = "567119031"        
    if cat == "erotik":
        b = "611339031"        
    if cat == "historisch":
        b = "610655031"        
    if cat == "ratgeber":
        b = "567131031"        
    if cat == "politik/geschichte":
        b = "567130031"    
    if cat == "jugendbuch":
        b = "4931127031"        
    if cat == "fachbuch":
        b = "567130031"
        
    url = "https://www.amazon.de/gp/bestsellers/digital-text/" + b + "/"
    print "Processing: "+url
    extracted_data = extracted_data + AmazonParserLinks(url)

    url = "https://www.amazon.de/gp/bestsellers/digital-text/" + b + "/#2"
    print "Processing: "+url
    extracted_data = extracted_data + AmazonParserLinks(url)

    url = "https://www.amazon.de/gp/bestsellers/digital-text/" + b + "/#3"
    print "Processing: "+url
    extracted_data = extracted_data + AmazonParserLinks(url)

    url = "https://www.amazon.de/gp/bestsellers/digital-text/" + b + "/#4"
    print "Processing: "+url
    extracted_data = extracted_data + AmazonParserLinks(url)

    url = "https://www.amazon.de/gp/bestsellers/digital-text/" + b + "/#5"
    print "Processing: "+url
    extracted_data = extracted_data + AmazonParserLinks(url)
    print len(extracted_data)
    
    return list(set(extracted_data))


########################### COLLECT BESTSELLERS ################################## 
 
def CollectBestsellers(cat):
  filename = str(time.strftime("%Y-%m-%d")) + "_bestseller.json"
  #filename = "2016-11-03" + "_bestseller.json"
  if os.path.isfile(filename):
      print "we already have fetched for that keyword!"
      with open(filename) as data_file:    
	  data = json.load(data_file)
	  #print data
	  links = data
  else:
      links = collectLinks()
      save(links,'bestseller')
  
  if not links:
	print "No links fetched."

  return links
 


################### READ PAGE ############################

def getPage(url):
    global hindex
    global last
#    print "     hindex " + str(hindex) + "\n"
#    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    #Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0
    #Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36
    headers = []
    #headers.append({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'})
    #headers.append({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0'})
    #headers.append({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'})
    headers.append({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    
    #headers.append({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'})

    
    hlist = ['Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
             'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
             'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
             'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
             'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
             'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko',
             'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
             'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
             'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36']
    
    tries = 0  
    while(True):
        try:  
            h = headers[0]
            
            
	    if(tries%2 == 0):
              tries = tries+1
	      page = requests.post(url,data={'u': url},headers=h,timeout=10)
	    else:
              tries = tries+1
	      page = requests.get(url,headers=h)

	    if "kein Bot sind" in page.content:
	      	patience = randint(1,3)
		print "- CAPTCHA - Retry in " + str(patience) + " seconds"
                hindex= hindex+1
                hindex = hindex%len(hlist)
                headers = []
                headers.append({'UserAgent': hlist[hindex]})
                #print "    change to " + str(hindex) + ". header " + str(headers[0])
                sleep(patience)
		continue
	    else:
		break
	except Exception as e:
	      print "Error in connecting to page:"
	      print e
	      print "Retry in 60 seconds.\n"
	      sleep(60)
	      continue
    return page


################### COLLECT LINKS FOR KEYWORD ############################

def AmazonParserLinks(url):
    print "Get links from page " + url + "."
    while True:
        try:
	    page = getPage(url)
	    AsinList = []    
	    print "Connected. Fetching link content from website."
            doc = html.fromstring(page.content)
            if "To discuss automated access to Amazon data please contact" in page.content:
                print "Blocked by amazon. Retry in 30s."
                sleep(30)
                continue
	    if len(page.content) < 1000:
		print "That seems like there was not much there: "
		print page.content[:2000]
		print "Retry in 30 seconds.\n"
		sleep (30)
		continue
	    XPATH_LINKS = '/html/body//a[contains(@href,'"amazon.de"')]/@href'
	    RAW_LINKS = doc.xpath(XPATH_LINKS)
	    for i in RAW_LINKS:
	      if "/dp/" in i:
		  dp = i.split("/dp/")[1]
		  dp = dp.split("/")[0]
		  if "?ref" in dp:
		    dp = dp.split("?ref")[0]
		  if dp not in AsinList:
                    if not "aaxitk" in dp:
                        if len(dp)>10:
                            dp = dp.split("#")[0]
                            #print dp
                        AsinList.append(dp)
	    if len(AsinList) == 0:
		print "No (more) links on result page found"	
#		with open ("pageError.html", "w") as f:
#		      f.write(page.content)
		return []
	    else: 
		return AsinList
	    
        except Exception as e:
            print e
            print "Retry in 30 seconds.\n"
	    sleep(30)
	    continue
    

#################### READ CONTENT FROM AMAZON PAGE ###########################################

def AmzonParser(url,asin,session):
    global hindex
    tries = 0 
    while(True):
	try: 
	      #print "Scraping page " + url
	      tries = tries+1
	      page = getPage(url)
	      if "Seite konnte nicht gefunden" in page.content:
			print "page is not found by Amazon. Skip."
			return
	      if "kein Bot sind" in page.content:
		  print "Captcha. Retry in 60 seconds.\n"
		  sleep(60)
		  continue
	      the_page = page.content
              #print the_page
#		  with open ("page.html", "w") as f:
#		      f.write(page.content)
	      the_page.replace("%20", " ")
	      if "<noscript>" in the_page:
		    content = the_page.split("<noscript>")[2]
		    content = content.split("</noscript>")[0]
		    content = clean_html(content)
		    if "#Detail_nav-sitewide" in content:
		      try:
			content = the_page.split("<noscript>")[3]
			content = content.split("</noscript>")[0]
			content = clean_html(content)
			#print content
		      except Exception as e:
			print "No blurb was found"
			content = ""
		    #print "Data and Blurb are accessible."
		    break
	      else:
		 print "no noscript"
		 if tries > 2:
                     #print the_page
                     return
#		 print "Retry in 2 seconds.\n"
		 hindex = hindex+1
#		 sleep(2)
		 continue
	except Exception as e:
		print "Exception occured while reading the page: "	
		print e    
		if tries > 5:
			return        
	  
    try:
	  doc = html.fromstring(page.content)
	  XPATH_NAME = '//h1[@id="title"]//text()'
	  XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Preis")]/following-sibling::td/text()'
	  XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
	  XPATH_AUTHOR = '//span[@class="author notFaded"]//text()'
	  XPATH_PRODUCTINFO = '//div[@class="content"]//text()'
	  XPATH_KU = '//span[@id="tmm-ku-upsell"]//text()'
	  XPATH_SALES = '//li[@id="SalesRank"]//text()'
	  XPATH_MORE = '//div[@id="biss-product-description-and-details"]//text()'
	  XPATH_PRICE = '//span[@class="a-button-inner"]//text()'
	  
	  RAW_MORE = doc.xpath(XPATH_MORE)
	  RAW_NAME = doc.xpath(XPATH_NAME)
	  RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
	  RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
	  RAW_AUTHOR = doc.xpath(XPATH_AUTHOR)
	  RAW_INFO = doc.xpath(XPATH_PRODUCTINFO)
	  RAW_KU = doc.xpath(XPATH_KU)
	  RAW_SALES = doc.xpath(XPATH_SALES)
	  RAW_PRICE = doc.xpath(XPATH_PRICE)
	  
	  if not RAW_NAME:
	    print "ERROR: Page cannot be parsed."
	    return
	  
	  NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
	  CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
	  ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None     
	  AUTHOR = ' '.join(''.join(RAW_AUTHOR).split()) if RAW_AUTHOR else None
	  INFO = ' '.join(''.join(RAW_INFO).split()) if RAW_INFO else None
	  KU = ' '.join(''.join(RAW_KU).split()) if RAW_KU else None
	  SALES = ' '.join(''.join(RAW_SALES).split()) if RAW_SALES else None
	  PRICE = ' '.join(''.join(RAW_PRICE).split()) if RAW_PRICE else None
	  
	  if not SALES:
	    firstrank = 0
	    firstcategory = ""
	    secondrank = 0
	    secondcategory = ""
	    thirdrank = 0
	    thirdcategory = ""
	  else: 
	    if '} Nr. ' in SALES:
		SALES = SALES.split('} Nr. ')[1]
		firstrank = int(SALES.split(' ')[0])
		firstcategory = SALES.split(' in ')[1]
		firstcategory = firstcategory.split(' Nr.')[0]
	      
		if ' Nr. ' in SALES:
		  SALES2 = SALES.split(' Nr. ')[1]
		  secondrank = int(SALES2.split(' ')[0])
		  secondcategory = SALES2.split(' in ')[1]
		  if ' Nr. ' in SALES2:
		      SALES3 = SALES2.split(' Nr. ')[1]
		      thirdrank = int(SALES3.split(' ')[0])
		      thirdcategory = SALES3.split(' in ')[1]    
		  else:
		      thirdrank = 0
		      thirdcategory = ""
		else: 
		  secondrank = 0
		  secondcategory = ""
		  thirdrank = 0
		  thirdcategory = ""
	    else:
	      firstrank = 0
	      firstcategory = ""
	      secondrank = 0
	      secondcategory = ""
	      thirdrank = 0
	      thirdcategory = ""
	  
    
	  if KU:
	    unlimited = 1
	  else:
	    unlimited = 0
	  
	  AUTHOR = AUTHOR.split(' (Autor)')[0]
	  
	  if ORIGINAL_PRICE is not None:
	    #print ORIGINAL_PRICE
	    PRICE = ORIGINAL_PRICE.split('EUR ')[1]
	    PRICE = PRICE.split(',')[0] + "." + PRICE.split(',')[1]
	    pricing = float(PRICE)
	  else:
	    if "EUR" in PRICE:
	      PRICE = PRICE.split('EUR ')[1]
	      PRICE = PRICE.split(' ')[0]
	      PRICE = PRICE.split(',')[0] + "." + PRICE.split(',')[1]
	      pricing = float(PRICE)
	  
	  if "Seitenzahl" in INFO: 
	      LENGTH = INFO.split('Seitenzahl der Print-Ausgabe: ')[1]
	      LENGTH = LENGTH.split(' Seiten')[0]
	      pages = int(LENGTH)
	  else:
	      pages = 0
	      
	  RATING = INFO.split('Durchschnittliche Kundenbewertung: ')[1]
	  RATING = RATING.split('Amazon')[0]

	  
	  if "Schreiben Sie" in RATING:
	    rezensionen = 0
	    bewertung = 0.0
	  else:
	    bewertung = float(RATING.split(' von')[0])
	    ratings = RATING.split(' Kundenrezension')[0]
	    ratings = ratings.split(' Sternen ')[1]
	    if "." in ratings:
		rezensionen = int(ratings.split(".")[0] + ratings.split(".")[1])		  
	    else:
		rezensionen = int(ratings)
	  

	  if page.status_code!=200:
	      raise ValueError('captha')
	  date = str(time.strftime("%d/%m/%Y"))
	  
	  if "} " in AUTHOR:
            AUTHOR = AUTHOR.split("} ")[1]
            
	  if " (" in AUTHOR:
            AUTHOR = AUTHOR.split(" (")[0]
            
	  if "," in AUTHOR:
            AUTHOR = AUTHOR.split(",")[0]

	  print "-SUCCESS- Fetched all the data."
	  data = {
		  'NAME':NAME,
		  'CATEGORY':CATEGORY,
		  'PRICE':pricing,
		  'BLURB':content,
		  'AUTHOR':AUTHOR,
		  'URL':url,
		  'PAGES':pages,
		  'REZENSIONEN':rezensionen,
		  'RATING':bewertung,
		  'KU': unlimited,
      '1RANK':firstrank,
		  '1CATEGORY':firstcategory,
		  '2RANK':secondrank,
		  '2CATEGORY':secondcategory,
		  '3RANK':thirdrank,
		  '3CATEGORY':thirdcategory,
		  'DATE' : date,
		  }

	  
	  return data
    except Exception as e:
	  print e
 
 
 
 ########## save ############
 
def save(links,keyword):
   filename = keyword + ".json"
   with open (filename, "w") as f:
      f.write(json.dumps(links))
   
 
 
 
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

 
 
 
 
 
 
 
 
################################# MAIN SEARCH METHOD #########################################
 
 
def ReadAsin(cat, bestsellers):
    global keycloud
    global last
    global title
    global pagedepth
    
    database = []
    second = []
    
    
    
    filename = "scrape-database-" + title + ".json"
    
    if os.path.isfile(filename):	
        try:
            with open(filename, 'rb') as f:
                database = json.load(f)
                print "database restored"
        except:
            with open(filename, 'rb') as f:
                database = pickle.load(f)
                print "database restored"
    else:
      print "started new database"

    if bestsellers == "y":
        keycloud.insert(0,["bestsellers"])
    print keycloud

    for k in range(0,len(keycloud)):
           neu = []
#           print "====================================================="
#           print "keyword group " + str(k+1) + " " + title
#           print "====================================================="
           for j in range(0,len(keycloud[k])):
               filename = "save-" +keycloud[k][j] + ".json"
               
               
               ###For every keyword,  
               if os.path.isfile(filename):	

                    if keycloud[k][j] == "bestsellers":
                      print "\n-------------------------------------------------------------------------------"
                      print "Loading bestsellers"
                      print "-------------------------------------------------------------------------------\n"

                    else:
                      print "\n-------------------------------------------------------------------------------"
                      print "Working on keyword \"" + keycloud[k][j] + "\" (" + str(j+1) + " of " + str(len(keycloud[k])) + ")"
                      print "-------------------------------------------------------------------------------\n"
                    #print "we already have a file"                
                    try:
                        with open(filename, 'rb') as f:
                            neu = json.load(f)
                            print "restored json " + str(k+1) + " " + keycloud[k][j] + str(len(neu)) + " " + filename
                    #        for a in range(0,10):
                    #                  print neu[a]["KEYWORDS"]
                    except:
                        with open(filename, 'rb') as f:
                            neu = pickle.load(f)
                            print "restored pickle " + str(k+1) + " " + keycloud[k][j] + str(len(neu)) + " " + filename
                            print len(database)
                     #       for a in range(0,10):
                     #                 print neu[a]["KEYWORDS"]
                    
                                        
                    app = 0
                    for n in range(0, len(neu)):
                        found = False
                        for i in range (0, len(database)):
                            if neu[n]["NAME"] == database[i]["NAME"]:
                                if not neu[n]["KEYWORDS"] == database[i]["KEYWORDS"]:
                                    for x in range(0, len(neu[n]["KEYWORDS"])):
                                        if neu[n]["KEYWORDS"][x] not in database[i]["KEYWORDS"]:
                                            database[i]["KEYWORDS"].append(neu[n]["KEYWORDS"][x])
                       #         try:
                       #             print neu[n]["NAME"][:30] + " == "+ database[i]["NAME"][:30]
                       #         except:
                       #             "found something"
                                found = True
                        if not found:
                            database.append(neu[n])
                            app = app +1
                    print str(app) + " entries appended."
                    with open('database.json', 'wb') as f:
                        print str(len(database)) + " books in total collected."
                        print "Database saved\n"
                        pickle.dump(database, f)
                            
               else:
                
                    if keycloud[k][j] == "bestsellers":
                      print "\n-------------------------------------------------------------------------------"
                      print "Fetching bestsellers"
                      print "-------------------------------------------------------------------------------\n"

                    else:
                      print "\n-------------------------------------------------------------------------------"
                      print "Working on keyword \"" + keycloud[k][j] + "\" (" + str(j+1) + " of " + str(len(keycloud[k])) + ")"
                      print "-------------------------------------------------------------------------------\n"

                    links = []
                    if keycloud[k][j] == "bestsellers":
                      links = CollectBestsellers(cat)
                    
                    
                    else:  
                      links = collectLinksForKeyword(keycloud[k][j])
                    #print links
                    
                    before = len(database)
                    
                    for l in range(0,len(links)): 
                      #for all the links found for this keyword, fetch all the books and append them to the database

                      s = requests.Session()
                      url = "https://www.amazon.de/dp/" + links[l]
                      found = False
                      print "Fetching Link " + str(l) + " of " + str(len(links)-1) + " for keyword " + str(j+1) + " of " + str(len(keycloud[k])) + " for keygroup " + str(keycloud[k][0])
                      

                      for i in range(0, len(database)):
                            if database[i]["URL"] == url:
                                  print "--> We already have an entry with that url: " + url + "\n"
                                  found = True
                                  key = database[i]["KEYWORDS"]
                                  if  keycloud[k][j] in key:
                                      n = 0 #do nothing
                                      #print "Entry already has the key.\n"
                                  else:
                                      #print "Updated keywords for entry.\n"
                                      if keycloud[k][j] not in database[i]["KEYWORDS"]:
                                        database[i]["KEYWORDS"].append(keycloud[k][j])
                      
                      if found == False:
                              ## new book url
                              data = AmzonParser(url,links[l],s)
                              if data:
                                    new = True
                                    for i in range(0, len(database)):
                                        ##already have a book with that title
                                        if database[i]["NAME"] == data["NAME"].encode('utf-8'):
                                              new = False
                                              print "we have that already"
                                              key = database[i]["KEYWORDS"]
                                              if  keycloud[k][j] in key:
                                                n = 0 #do nothing
                                                  #print "Entry already has the key.\n"
                                              else:
                                                  #print "Updated keywords for entry.\n"
                                                  #print "adding new key " +  keycloud[k][0]
                                                  if keycloud[k][j] not in database[i]["KEYWORDS"]:
                                                    database[i]["KEYWORDS"].append(keycloud[k][j])
                                    if new == True:
                                              ## new book title as well!
                                              
                                              if (excludeBundles == 1):
                                                if " band " in data["NAME"].lower() or "sammelband" in data["NAME"].lower() or "bundle" in data["NAME"].lower() or " collection" in data["NAME"].lower() or " serie "  in data["NAME"].lower() or " reihe " in data["NAME"].lower():
                                                  print data["NAME"] + " was not added because it's a bundle.\n\n"
                                                  continue;
                                              
                                              if (excludeBad == 1):
                                                if (data["REZENSIONEN"] > 0 and  data["RATING"] < 3):
                                                   print data["NAME"] + " was not added because it's rating is to low.\n\n"
                                                   continue;
                                                 
                                              if (excludeUnreviewed == 1):
                                                if (data["REZENSIONEN"] == 0):
                                                   print data["NAME"] + " was not added because it doesn't have reviews.\n\n"
                                                   continue;
                                                 
                                              if (KU == 1):
                                                if (data["KU"] == 0):
                                                   print data["NAME"] + " was not added because it is not in Kindle Unlimited\n\n"
                                                   continue;
                                                 
                                              if (KU == 2):
                                                if (data["KU"] == 1):
                                                   print data["NAME"] + " was not added because it is in Kindle Unlimited\n\n"
                                                   continue;
                                                  
                                              
                                              data["KEYWORDS"] = []
                                              data["KEYWORDS"].append(keycloud[k][j])
                                              #print data
                                              for a in range(0,len(keycloud)):
                                                for b in range (0, len(keycloud[a])):
                                                  if keycloud[a][b] in data["NAME"]:
                                                    if keycloud[a][b] not in data["KEYWORDS"]:
                                                      data["KEYWORDS"].append(keycloud[a][b])
                                                  if keycloud[a][b] in data["BLURB"]:
                                                    if keycloud[a][b] not in data["KEYWORDS"]:
                                                      data["KEYWORDS"].append(keycloud[a][b])
                                              try:
                                                print data["NAME"]
                                              except:
                                                print "Another book"
                                              print str(data["PAGES"]) + " Pages, Keywords: " + str(data["KEYWORDS"])
                                              print "-->APPENDED TO DATABASE\n"
                                              database.append(data)
                    
                    print "\n-------------------------------------------------------------------------------"
                    print "Finished on keyword \"" + keycloud[k][j] + "\" (" + str(j+1) + " of " + str(len(keycloud[k])) + " for keygroup " + str(keycloud[k][0]) + "): found " + str((len(database))-before) + " new entries."
                    print "-------------------------------------------------------------------------------\n\n"
                    
                    
                    filename = "scrape-database-" + title + ".json"
                        
                    with open(filename, 'wb') as f:
                        print str(len(database)) + " books in total collected."
                        print "Database saved\n"
                        pickle.dump(database, f)


    for i in range (0, len(database)):
     #   print "story " + str(i)
        try:
            database[i]["NAME"] = database[i]["NAME"].encode('utf-8')
        except:
            o = 19
        try:
            database[i]["AUTHOR"] = database[i]["AUTHOR"].encode('utf-8')
        except:
            o = 19
        try:
            database[i]["BLURB"] = database[i]["BLURB"].encode('utf-8')
        except:
            o = 19
        try:
            database[i]["1CATEGORY"] = database[i]["1CATEGORY"].encode('utf-8')
        except:
            o = 19
        try:
            database[i]["2CATEGORY"] = database[i]["2CATEGORY"].encode('utf-8')
        except:
            o = 19
        try:
            database[i]["3CATEGORY"] = database[i]["3CATEGORY"].encode('utf-8')
        except:
            o = 19
            
      
    filename = title + ".json"
        
    with open(filename, 'wb') as f:
        print str(len(database)) + " books in total collected."
        print "Database saved\n"
        pickle.dump(database, f)
        
        
  
    writeToCSV(database)
                    
   
    
    
if __name__ == "__main__":
  
  
  filename = "config"
  if os.path.isfile(filename):
      with open(filename) as data_file:
        try:
          configs = json.load(data_file)
          pagedepth = configs[0][1]
          excludeBundles = configs[1][1]
          excludeUnreviewed = configs[2][1]
          excludeBad = configs[3][1]
          KU = configs[4][1]
          if not (excludeBad in [0,1] and excludeUnreviewed in [0,1] and excludeBundles in [0,1] and KU in [0,1,2] and isinstance(pagedepth, int) and pagedepth > 0 and pagedepth < 100):
            print "Config file has errors. Fix it, or delete it before starting again."
            sys.exit()
        except:
          print "Config file has errors. Fix it, or delete it before starting again."
          sys.exit()
  
  
  else:
      print "config file deleted. Using defaults."
      configs = []
      pages = ["result pages: ", 6]
      excludeBundles = ["exclude bundles: ",0]
      excludeUnreviewed = ["exlude unreviewed books: ", 0]
      excludeBad = ["exlude bad books: ", 0]
      KU = ["kindle unlimited: ", 0]
      configs.append(pages)
      json.dumps(configs)        
      with open (filename, "w") as f:
          f.write(json.dumps(configs))
      pagedepth = 6
  
  if len(sys.argv) < 2:
      print "You must set at least two arguments. The first one specifies the name of your search, the second and all subsequent are the search keywords.\n"
      print "e.g. python scrape.py krimi-suche krimi mord detektiv" 
      sys.exit()
  else:
      title = sys.argv[1]
      key = []
      for i in range(2, len(sys.argv)):
        key.append(sys.argv[i])
      keycloud.append(key)
      

  cat = " "
  bestsellers = "x"
  categories = ["krimi/thriller","gegenwart","fantasy/scifi","liebe","erotik","historisch","ratgeber","politik/geschichte","jugendbuch","fachbuch","none"]
  
      
  
  while cat not in categories:
    cat = raw_input("Pick a subcategory on Amazon to limit your search to (better results, especially for genre fiction). Options: 'krimi/thriller','gegenwart','fantasy/scifi','liebe','erotik','historisch','ratgeber','politik/geschichte','jugendbuch','fachbuch','none'\n")
  
  
  if cat == "none":
    while bestsellers not in ["y","n"]:
      bestsellers = raw_input("Do you want to include the bestsellers of the general kindle shop? (regardless of whether the match the search terms) y/n\n")
  else:
    while bestsellers not in ["y","n"]:
      bestsellers = raw_input("Do you want to include the bestsellers of your category? (regardless of whether the match the search terms) y/n\n")

  ReadAsin(cat, bestsellers)

