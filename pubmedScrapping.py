#!/usr/bin/env python
# coding: utf-8

# In[4]:


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


# In[8]:


def scrapping():
    
    ### build the driver
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", '/')
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf,application/x-pdf")

    profile.set_preference("pdfjs.disabled", "true")

    executable_path = '/Users/charleschen/Downloads/geckodriver'
    driver = webdriver.Firefox(executable_path = executable_path, firefox_profile = profile)

    ### Get the main website
    
    # Set the key word after "term="
    driver.get("https://search.crossref.org/?q=Life+Science+Physiology+PMC")
    
    ### Click the Free Full Article link
    
    fullArticleLink = driver.find_element_by_link_text("Free full text")
    fullArticleLink.click()
    #print("free full article link clicked.")
    
    ### For loop for pageNum pages of PMC articles
    
    pageNum = 3    # The number of pages to be scraped
    i = 0
    
    for i in range(pageNum):
        
        ### Read all the free PMC articles in this page and follow the link to article page
        k = 0    # counter for the number of articles
        rawTitles = driver.find_elements_by_link_text("Free PMC Article")
        rawLinks = []
        title = ""
        
        for rawTitle in rawTitles:
            driver1 = webdriver.Firefox(executable_path=executable_path)
            url = (rawTitle.get_attribute("href"))
            
            ### Going to article page

            driver1.get(url)
            time.sleep(3)

            actualArticlePages = driver1.find_elements_by_xpath("//div[@class = 'icons portlet']/a")
            
            if(len(actualArticlePages) != 0):
                ### Find the link for PMC, not other journals
                actualArticlePage = actualArticlePages[-1]
                
                ### Find the title of the article
                
                title = driver1.find_elements_by_xpath("//div[@class = 'rprt abstract']/h1")[0].text
                
                ### Find the journal of the article, in case needed for further usage
                #journal = actualArticlePage.get_attribute("journal")
                #print(journal)
                
                ### Get the article name
                name = title+"pdf"
                
                k = k + 1
                
                ### "Further usage: get articles from journals other than PMC
                #if journal =="Cells" or journal == "Vaccine" or journal == "BMJ Open" or journal == "Biotechnol Biofuels" or journal == "Asian-Australas J Anim Sci":
                
                ### Go to actual download page
                
                actualDownloadUrl = actualArticlePage.get_attribute("href")
                #print("Download Page: ",actualDownloadUrl)
                driver1.get(actualDownloadUrl)
                
                ### Going to the actual download page
                if "PDF" in driver1.page_source:
                    #print("PDF found!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    downloadNode = driver1.find_element_by_partial_link_text("PDF")
                    download_url = downloadNode.get_attribute("href")
                    #print ("download URL: ", download_url)
                    
                    ### Set header for requests, currently Firefox header used
                    
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                    res = requests.get(download_url, allow_redirects=True, headers = headers)
                    
                    # pdf will be downloaded in the same folder as the program
                    with open(name.replace("/"," or "), 'wb') as f:
                        f.write(res.content)
                    #time.sleep(3)
                    print("Successfully downloaded article ",k ,"in the current page!")
                    
                    ### Close the current driver
                    driver1.close()
                else:    
                    print("No link found.")
                # End of outer if
            # End of outer For for the current page
            
        ### Get to the next page
        print("Finish scraping the current page.")
        nextPage = driver.find_elements_by_xpath("//a[@class = 'active page_link next']")[0]
        if nextPage:
            nextPage.click()
        else:
            break
        #End of outer for
    print("Finish downloading")


# In[9]:


if __name__ == "__main__":
    scrapping()


# In[103]:


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
res = requests.get("https://arxiv.org/pdf/1509.02971.pdf", allow_redirects=True, headers = headers)
#res.headers['content_type'] = 'application/pdf'

with open(name+".pdf", 'wb') as f:
    # 1.
    f.write(res.content)


#     2.
#     for chunk in f.iter_content(chunk_size = 1024):
#         if chunk:
#             f.write(chunk)

#     res.raise_for_status()
#     playFile = open(name+".pdf", 'wb')
#     for chunk in res.iter_content(100000):
#             playFile.write(chunk)
#     playFile.close()

#     3.
#     #wget.download(download_url, "/")
#     driver1.get(download_url)

#     insideDownload_url = 

#     4.
#     rslt = requests.get(download_url)
#     print("Got ", rslt)
#     with open(name+".pdf", "wb") as fout:
#         fout.write(res.raw.read())


# In[7]:


print(type(nextPage))


# In[ ]:




