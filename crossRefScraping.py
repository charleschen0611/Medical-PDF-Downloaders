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
    
    fullArticleLink = driver.find_element_by_partial_link_text("Journal Article")
    fullArticleLink.click()
    #print("free full article link clicked.")
    
    ### For loop for pageNum pages of PMC articles
    
    pageNum = 10    # The number of pages to be scraped
    i = 0
    title = ""
    for i in range(pageNum):
        
        ### Read all the free PMC articles in this page and follow the link to article page
        k = 0    # counter for the number of articles
        rawTitles = driver.find_elements_by_xpath("//div[@class = 'item-links']/a")
        titles = driver.find_elements_by_class_name("lead")
        #rawLinks = []
        j = 0
#         initialLinks = []
        for rawTitle in rawTitles:
            
            # skip the link of multiple citations
            if len(rawTitle.find_elements_by_class_name("icon-resize-small")) == 0:
            
                driver1 = webdriver.Firefox(executable_path = executable_path)
                #print("link: ",rawTitle.get_attribute("href"))
                #initialLinks.append(rawTitle.get_attribute("href"))
                url = (rawTitle.get_attribute("href"))

                ### Going to article page

                driver1.get(url)
                time.sleep(3)

                print("The No.", j, " article")
                title = titles[j].text
                j = j + 1

                ### Find the journal of the article, in case needed for further usage
                #journal = actualArticlePage.get_attribute("journal")
                #print(journal)

                ### Get the article name
                name = title+".pdf"


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

                    k = k+1
                    print("Successfully downloaded article ",k ,"in the current page!")

                    ### Close the current driver
                    driver1.close()
                else:    
                    print("No link found.")


                if j > 10:
                    break
                    ######### 再改!!!!!!!!!!!!!!!!!!!!!!
            
        
        ### Get to the next page
        print("Finish scraping the current page.")
        nextPage = driver.find_elements_by_xpath("//li[@class = 'next next_page ']/a")[0]
        if nextPage:
            time.sleep(1)
            nextPage.click()
        else:
            break
        #End of outer for
    print("Finish downloading")


# In[ ]:


if __name__ == "__main__":
    scrapping()


# In[7]:


print(type(rawTitle))


# In[ ]:


# Actual pdf page 

    
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
                
                title = driver.findElement(By.xpath("//div[contains(text(),'"+"title"+"')]")).text;
                
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
            


# In[ ]:




