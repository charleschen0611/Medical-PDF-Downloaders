#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


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
    
    # Set the key word after "for=", before "&sort="
    driver.get("https://elifesciences.org/subjects/neuroscience")
    print(0)
#     ### Click the Free Full Article link
    
#     fullArticleLink = driver.find_element_by_link_text("Free full text")
#     fullArticleLink.click()
#     #print("free full article link clicked.")
    
    ### For loop for pageNum pages of PMC articles
    
    pageNum = 2    # The number of pages to be scraped
    i = 0
    k = 0
    j = 1       # counter for the number of pages to be scraped
    
    ### Click Load More button for pageNum-1 times
    
    for i in range(pageNum):
        print("Loading additional articals.")
        nextPage = driver.find_element_by_xpath("//a[@class = 'button button--default button--full']")
        if nextPage:
            driver.execute_script("arguments[0].click();", nextPage)
            time.sleep(3)
        #nextPage.click()
    

    
    rawTitles = driver.find_elements_by_xpath("//a[@class = 'teaser__header_text_link']")
    print(len(rawTitles))
    
    title = ""
    #print(1)
    for rawTitle in rawTitles:
        driver1 = webdriver.Firefox(executable_path=executable_path)
        url = (rawTitle.get_attribute("href"))

        ### Going to article page

        driver1.get(url)
        time.sleep(3)
        #print(2)
        actualArticlePages = driver1.find_elements_by_xpath("//a[@class = 'content-header__download_link']")
        #print(3)
        if(len(actualArticlePages) != 0):
            ### Find the link for PMC, not other journals
            actualArticlePage = actualArticlePages[-1]
            #print(4)
            ### Find the title of the article

            title = driver1.find_elements_by_xpath("//div[@class = 'content-header__body']/h1")[0].text
            #print(5)
            ### Find the journal of the article, in case needed for further usage
            #journal = actualArticlePage.get_attribute("journal")
            #print(journal)

            ### Get the article name
            name = title+".pdf"

            k = k + 1

            ### "Further usage: get articles from journals other than PMC
            #if journal =="Cells" or journal == "Vaccine" or journal == "BMJ Open" or journal == "Biotechnol Biofuels" or journal == "Asian-Australas J Anim Sci":

            ### Go to actual download page
            actualArticlePage.click()

#                 actualDownloadUrl = actualArticlePage.get_attribute("href")
#                 print("Download Page: ",actualDownloadUrl)
#                 driver1.get(actualDownloadUrl)

            ### Going to the actual download page
            if "PDF" in driver1.page_source:
                print("PDF found in the current page")
                downloadNode = driver1.find_elements_by_class_name("article-download-links-list__link")[0]
                download_url = downloadNode.get_attribute("href")
                print ("download URL: ", download_url)

                ### Set header for requests, currently Firefox header used

                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                res = requests.get(download_url, allow_redirects=True, headers = headers)
                #print("@@@",res.content)
                # pdf will be downloaded in the same folder as the program
                open(name.replace("/"," or "), 'wb').write(res.content)
                #time.sleep(3)
                print("Successfully downloaded article ",k ,"in the current page!")

                ### Close the current driver
                driver1.close()
            else:    
                print("No link found.")
            # End of outer if
        # End of outer For for the current page
        j = j +1
        #End of outer for
    print("Finish downloading")


# In[3]:


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


# In[ ]:




