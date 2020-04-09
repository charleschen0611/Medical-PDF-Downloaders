#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# import statements
import requests
import pandas as pd
import matplotlib.pyplot as plt
import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#from urllib.request import urlretrieve
# from requests import get
import urllib
#import urllib.request

import time

import wget

from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
#driver = webdriver.Firefox(FIREFOXDRIVER_PATH, firefox_options=options)

s = requests.session()
s.keep_alive = False

from datetime import datetime

import os


# In[11]:


def scraping():
    
    
    #response = requests.get('https://www.baidu.com', proxies={'https':'https://175.171.110.49:53281'})
    
    ### build the driver for downloading PDF 
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")

    profile.set_preference("pdfjs.disabled", "true")

    executable_path = '/Users/charleschen/Downloads/geckodriver'
    
    ### For loop for pageNum pages of all articles with OPEN access
    
    pageNum = 460#444    # The number of pages to be scraped
    
    numOpen = 1    # The number of pages opened          
    k = 0          # counter for the total number of articles
    l = 426
    # The starting page to be scraped, initially set to 1.
    
    # Record the time of start
    now = datetime.now()
    
    for i in range(l, pageNum+1):
        m = 0   # The number of articles download in the current page
        print("Scraping Page", str(i))
        driver = webdriver.Firefox(executable_path = executable_path)
        
        ### Get the main website
        
        # Set the key word after "q=" and before "&page="
        address = "https://journals.plos.org/plosone/search?filterJournals=PLoSONE&filterJournals=PLoSMedicine&filterJournals=PLoSNTD&filterSections=Abstract&filterSections=Title&q=epidemiology&page=" + str(i)
        driver.get(address)
        time.sleep(5)
        #print(address)
        ### Read all the articles in this page and follow the link to article page
        
        rawTitles = driver.find_elements_by_xpath("//dt/a")
#         print(rawTitles[0])
#         print(1)
        
        rawTitles.reverse()
        rawLinks = []
        title = ""
        
        # Get all the links of the titles and go to actual download page
        for num, rawTitle in enumerate(rawTitles):
            print(2)
            driver1 = webdriver.Firefox(executable_path=executable_path)
#             link = rawTitle.get_child("a")
            url = (rawTitle.get_attribute("href"))
            
            driver1.get(url)
            
           
        
            k = k +1
            
            # Get the title of the article
            if "title-authors" in driver1.page_source:
                title = driver1.find_element_by_xpath("//h1[@id = 'artTitle']").text[0:142]
                
#                 if len(title)>100:
#                     title = title[:99]
                
                name = title + ".pdf"
                #print("Article name: ", name)
            
            
            ### Going to the actual download page
            if "Download PDF" in driver1.page_source:
                
                print("PDF found!")
                downloadNode = driver1.find_element_by_partial_link_text("Download")
                download_url = downloadNode.get_attribute("href")
                #print ("download URL: ", download_url)
                
                # Beep once for finding a pdf
                beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
                beep(1)
                
                ### Set header for requests, currently Firefox header used
                
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                res = requests.get(download_url, allow_redirects=True, headers = headers)
                time.sleep(1)
                # pdf will be downloaded in the same folder as the program
                with open(name.replace("/"," or "), 'wb') as f:
                    f.write(res.content)
                time.sleep(1)
                m = m + 1
                print("Successfully downloaded article",  str(m),"in page", str(i),", in total", str(k), 
                      "articles downloaded in",str((i-l+1)), "pages.")    # ",", name,
                
                
            elif driver1.find_element_by_class_name("dload-pdf.no-pdf") is not None:
                print("No PDF download link available!")
                
            else:    
                print("No link found.")
            
            ### Quit the current driver    
            driver1.quit()
            # End of inner for
            
        print("Finish scraping the page ", str((i)))   
        
        # Beep three times after scraping each page
        beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
        beep(3)    
            
        ### Close the current driver    
        driver.quit()
        
        print("Time used for current page:")
        then = datetime.now()
        print(then-now)    
        ### Get to the next page
        
#         numOpen = numOpen + 1
#         nextPageLink = driver.find_element_by_id("nextPageLink").get_attribute("href")
#         if nextPageLink:
            
#             driver.get(nextPageLink)
            
#         else:
#             break
        #End of outer for
    
    then = datetime.now()
    print("Total time used:  ",str(then-now))
    
    beep = lambda x: os.system("echo -n '\a';sleep 0.2;" * x)
    beep(10)
    print("Finish downloading!")


# In[ ]:


if __name__ == "__main__":
    scraping()


# In[ ]:





# In[ ]:





# In[ ]:





# In[12]:


g = 1


# In[13]:


print(g)


# In[ ]:




