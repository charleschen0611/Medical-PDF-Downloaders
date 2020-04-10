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
from datetime import datetime

import wget


# In[9]:


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
    i = 0
    driver.get("https://cmjournal.biomedcentral.com/articles?searchType=journalSearch&sort=PubDate&page=10")
    print(0)
#     ### Click the Free Full Article link
    
#     fullArticleLink = driver.find_element_by_link_text("Free full text")
#     fullArticleLink.click()
#     #print("free full article link clicked.")
    
    ### For loop for pageNum pages of PMC articles
    
    pageNum = 2    # The number of pages to be scraped
    
    k = 0
    j = 1       # counter for the number of pages to be scraped
    
    ### Click Load More button for pageNum-1 times
    
    for i in range(pageNum):
        
        
        rawTitles = driver.find_elements_by_xpath("//h3[@class = 'c-listing__title']/a")
        print(len(rawTitles))

        title = ""
        print(1)
        for rawTitle in rawTitles:
            
            ### Record the time before scraping each article
            now = datetime.now()
            
            driver1 = webdriver.Firefox(executable_path=executable_path)
            url = (rawTitle.get_attribute("href"))

            ### Going to article page
            
            
            
            ### Check the status of Page
            page =requests.get(url)
            if page.status_code==200:
                
                driver1.get(url)

                time.sleep(3)
                print(2)
    #             actualArticlePages = driver1.find_elements_by_xpath("//a[@class = 'c-article-title u-h1']")
    #             print(3)
                if(1 != 0):
                    ### Find the link for PMC, not other journals
                    #actualArticlePage = actualArticlePages[-1]
                    print(4)
                    ### Find the title of the article

                    title = driver1.find_element_by_xpath("//h1[@class = 'c-article-title u-h1']").text
                    #print(5)
                    ### Find the journal of the article, in case needed for further usage
                    #journal = actualArticlePage.get_attribute("journal")
                    #print(journal)

                    ### Get the article name
                    name = title+".pdf"
                    print(name)
                    k = k + 1

                    ### "Further usage: get articles from journals other than PMC
                    #if journal =="Cells" or journal == "Vaccine" or journal == "BMJ Open" or journal == "Biotechnol Biofuels" or journal == "Asian-Australas J Anim Sci":

                    ### Go to actual download page
                    #actualArticlePage.click()

        #                 actualDownloadUrl = actualArticlePage.get_attribute("href")
        #                 print("Download Page: ",actualDownloadUrl)
        #                 driver1.get(actualDownloadUrl)

                    ### Going to the actual download page
                    if "PDF" in driver1.page_source:
                        print("PDF found in the current page")
                        downloadNode = driver1.find_elements_by_class_name("c-pdf-download__link")[0]
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
        print("Finish downloading")    
        print("Loading additional articals from page ",(i+1))
        
        then = datetime.now()
        print("Time used for the current page: ",str(then-now)) 
        
        nextPage = driver.find_elements_by_xpath("//a[@class = 'c-pagination__link']")[-1]
        if nextPage:
#             driver.execute_script("arguments[0].click();", nextPage)
#             time.sleep(3)
            nextPage.click()
    
            #End of outer for
    


# In[10]:


if __name__ == "__main__":
    scrapping()
