
# coding: utf-8

# # "I'll take 'Webscraping' for 400, Alex"
# 
# A look at webscraping clues from Jeopardy, 
# 
# by Matt Heckman & Brennan Donnell

# ## The goal of the project:
# 
# * Explore other webscraping alternatives
# * Test scraping of Jeopardy questions, or 'clues'. 
# * Given the categories of past games, can we classify our own questions?
# 

# ## Tools used: 
# 
# * Selenium for webscraping
# * Chromedriver (for automating the process). 
# * bayesText.py (from A10)
# * Xpath

# In[2]:


import numpy as np
import time
import re
import os
from bayesText import *
from IPython.display import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


# ## What is Selenium? 
# 
# Selenium is a webdriver that automates a browser to scrape information. 
# 
# ## Why use it over BeautifulSoup
# 
# Interactive elements on a webpage. 
# Initially we were going to look at more than just clue text, so this was necessary. 
# 
# ## What is 'xpath'
# 
# Point to a specific part of the page. A bit more precise than the BS4 method. 

# ## Webpage structure
# 
# This is what we were scraping, two per page. We got the *Categories* and then the *clues*, or the questions. 

# In[2]:


Image(filename='Screen Shot 2018-10-29 at 4.11.41 PM.png')


# ## The code: 
# 
# Purpose of the function: 
# Start at a game, and then scrape both the Jeopardy and Double Jeopardy tables, then move to the next page, until there are no more pages. Each time this is done, create a folder with the name of the category and then populate the folder with the questions as text files. 
# 
# **Note: we will show the full code after the presentation. Also, the function is too long to fit on a slide**. 

# In[6]:


def drive_jeopardy_clue():
    chromedriver = "/Users/brennandonnell/grad_school/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)
    count = 1
    driver.get("http://www.j-archive.com/showgame.php?game_id=2037")
#     driver.maximize_window() # It didn't like this. 
    while count < 6: #initially set to 300
        title_bs4 = driver.find_element_by_xpath('//*[@id="game_title"]/h1')
        print(title_bs4.text)
        for j in range(1, 7):
            category_bs4 = driver.find_element_by_xpath(
                '//*[@id="jeopardy_round"]/table[1]/tbody/tr[1]/td[' + str(j) +
                ']/table/tbody/tr[1]/td')
            category = category_bs4.text
            print('\t' + category)
            jeopardy_directory = "/Users/brennandonnell/grad_school/data900/Untitled Folder/Jeopardy_scraping/"
            if not os.path.exists(jeopardy_directory + category + '/'):
                os.makedirs(jeopardy_directory + category + '/')

            for i in range(1, 6):
                try:
                    clue_text_bs4 = driver.find_element_by_xpath(
                        '//*[@id="clue_J_' + str(j) + '_' + str(i) + '"]')
                    clue_text = clue_text_bs4.text
                    print('\t\t' + clue_text)
                    file = open(
                        jeopardy_directory + category + '/' + str(i) + ".txt",
                        "w")
                    file.write(clue_text)
                    file.close()
                except (NoSuchElementException):
                    print('no element')
        print('done with jeopardy, on to double jeopardy')
        for j in range(1, 7):
            category_bs4 = driver.find_element_by_xpath(
                '//*[@id="double_jeopardy_round"]/table[1]/tbody/tr[1]/td[' +
                str(j) + ']/table/tbody/tr[1]/td')
            category = category_bs4.text
            print('\t' + category)
            jeopardy_directory = "/Users/brennandonnell/grad_school/data900/Untitled Folder/Jeopardy_scraping/"
            if not os.path.exists(jeopardy_directory + category + '/'):
                os.makedirs(jeopardy_directory + category + '/')

            for i in range(1, 6):
                try:
                    clue_text_bs4 = driver.find_element_by_xpath(
                        '//*[@id="clue_DJ_' + str(j) + '_' + str(i) + '"]')
                    clue_text = clue_text_bs4.text
                    print('\t\t' + clue_text)
                    file = open(
                        jeopardy_directory + category + '/' + str(i) + ".txt",
                        "w")
                    file.write(clue_text)
                    file.close()
                except (NoSuchElementException):
                    print('no element')

        try:
            # add a wait
            next_page = driver.find_element_by_xpath(
                '//*[@id="contestants_table"]/tbody/tr/td[3]/a')
            actions = ActionChains(driver)
            actions.move_to_element(next_page)
            actions.click()
            actions.perform()
            count = count + 1
            print(count)
        except (NoSuchElementException):
            print('no new page')
            driver.close()
            break
    driver.close()
    return


# ## Running the code
# 
# Calling the `drive_jeopardy_clue()` function starts at Monday, September $8^{th}$, 2003, and then goes through the next $n$ games unless there is no *next game* button. 
# 
# For this demo, let $n=5$

# In[7]:


drive_jeopardy_clue()


# ## Classifying the clues
# 
# ### Restrictions
# * Time Constraints
# * Grouping of categories
# * Insufficient data for a full training & test

# In[6]:


baseDirectory = '/Users/brennandonnell/grad_school/data900/Untitled Folder/20news-bydate/'
trainingDir = baseDirectory + "archive_redux copy/"
testDir = baseDirectory + "20news-bydate-test/"
print('Stoplist 1')
bT = BayesText(trainingDir, baseDirectory + 'stopwords_bbc.txt')


# ## How does the model do? 

# In[8]:


print("Running Test ...")
class_path = '/Users/brennandonnell/grad_school/data900/Untitled Folder/20news-bydate/'
print("Classify post@classify1:", bT.classify(class_path + "classify_jeopardy3.txt"))
print("Classify post@classify2:", bT.classify(class_path + "classify_jeopardy2.txt"))
print("Classify post@classify3:", bT.classify(class_path + "classify_jeopardy4.txt"))
print("Classify post@classify4:", bT.classify(class_path + "classify_jeopardy1.txt"))


# ## The texts classified: 
# 

# ## The texts classified: 
# 
# * **First**: Nintendo's original handheld gaming device. (What is the GameBoy)

# ## The texts classified: 
# 
# * **Second**: This multi-film franchise takes place in a galaxy far far away. (What is Star Wars) 

# ## The texts classified: 
# 
# * **Third**: Michael Crichton's novel about genetically engineered dinosaurs. (What is *Jurassic Park*)

# ## The texts classified: 
# 
# * **Fourth**: This famous general became the first president of a fledgling nation after a war of independence and was unanimously elected. (Who is George Washington)

# ## Where to improve? 
# * Combine similar categories
# * Get more data
# * Set up a training/test set

# # Thank you
