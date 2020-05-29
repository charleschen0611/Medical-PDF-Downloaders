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

from datetime import datetime

from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
#driver = webdriver.Firefox(FIREFOXDRIVER_PATH, firefox_options=options)

import os


# In[32]:


def scrapping():
    
    ### build the driver
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")

    profile.set_preference("pdfjs.disabled", "true")

    executable_path = '/Users/charleschen/Downloads/geckodriver'
    
    # Record the start time of the project
    start = datetime.now()
    
    ### For loop for pageNum pages of all articles with OPEN access
    
    pageNum = 4   # The number of pages to be scraped
    l = 2          # The starting page number to read from
    j = 0          # The number of articles download in the current page
    k = 0          # The total number of articles visited  in the current page
    for i in range(l, pageNum+1):
        # Record the time of start for the current page
        now = datetime.now()
        
        print("Scraping Page ",str(l))
        
        driver = webdriver.Firefox(executable_path = executable_path, firefox_profile = profile)
        j = 1    # Reset j for the current page
        ### Get the main website
        
        # Set the key word after "q=" and before "&page="
        address = "https://www.preprints.org/search?search1=covid-19&field1=article_abstract&clause=AND&search2=&field2=authors&search_subject_area=&search_subject_sub_area=&date_from=2020-03-05&date_to=2020-05-07&search_btn=&page_num=" + str(l)
        driver.get(address)
        
        ### Read all the articles in this page and follow the link to article page
        
        rawTitles = driver.find_elements_by_xpath("//div/a[@class = 'title']")
        
        
        # Get all the links of the titles and go to actual download page
        for num, rawTitle in enumerate(rawTitles):
            
            driver1 = webdriver.Firefox(executable_path=executable_path)
            url = (rawTitle.get_attribute("href"))
            
            driver1.get(url)
            time.sleep(1)
           
            k = k + 1
            
            # Get the title of the article
            #if "c-article-title" in driver1.page_source:
            title = driver1.find_element_by_xpath("//div/h1").text

            # eliminate the Spqces

            name = title + ".pdf"
            #print("Article name: ", name)
            
            ### Going to the actual download page
            #if "PDF" in driver1.page_source:
                
            print("PDF found!")
            downloadNode = driver1.find_element_by_partial_link_text("Download PDF")
            download_url = downloadNode.get_attribute("href")
            #print ("download URL: ", download_url)

            ### Set header for requests, currently Firefox header used

            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            res = requests.get(download_url, allow_redirects=True, headers = headers)

            # pdf will be downloaded in the same folder as the program
            with open(name.replace("/"," or "), 'wb') as f:
                f.write(res.content)

            print("Successfully downloaded article ", j ,"in page "+str(l)+"! In total ", k, " articles downloaded")
            j = j + 1
            ### Close the current driver
            driver1.close()
#             else:    
#                 print("No link found.")
#                 # End of outer if
            
#                 driver1.close()
            
                # End of outer For for the current page
        
        print("Time used for current page:")
        then = datetime.now()
        print("Time used for the current page: ",str(then-now)) 
        
        ### Get to the next page
        print("Finish scraping page ", (l-1))
        
        nextPage = driver.find_elements_by_xpath("//ul[@class = 'pagination']/li/a")[-1]
        if nextPage:
            #nextPage = nextPage[-1]
            print("In if")
            nextPage.click()
            driver.close()
        else:
            print("In else")
            break
        #End of outer for
    end = datetime.now()
    print("Time used for this execution: ",str(end - start))
    print("Finish downloading!")
    
    os.system('say "Your Program has finished."')


# In[33]:


if __name__ == "__main__":
    scrapping()


# In[ ]:





# In[14]:


a = ["13", "2", "43"]
b = "2"
if b in a:
    a.remove(b)
print(a)


# In[21]:


profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", '/')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")

profile.set_preference("pdfjs.disabled", "true")

executable_path = '/Users/charleschen/Downloads/geckodriver'

driver = webdriver.Firefox(executable_path = executable_path, firefox_profile = profile)
address = "https://www.preprints.org/search?search1=covid-19&field1=article_abstract&clause=AND&search2=&field2=authors&search_subject_area=&search_subject_sub_area=&date_from=2020-03-05&date_to=2020-05-07&search_btn=&page_num=" + str(2)
driver.get(address)
preRawTitles = driver.find_elements_by_xpath("//div[@class = 'search-content-box margin-serach-wrapper-left']")

for preRawTitle in preRawTitles:
    title = preRawTitle.get_child("/div")
    print(len(title))
#     if len():
#         print("Got inside")


# In[ ]:




