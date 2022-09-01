from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Initalize WebDriver
driver = webdriver.Chrome('chromedriver.html')
# Open website for scraping
driver.get('https://ca.finance.yahoo.com/quote/')
# Grab company name
companies = driver.find_elements_by_xpath('//div@class="D(ib)"]')
# Adding company names to list
companies_list = []
for p in range(len(companies)):
    companies_list.append(companies[p].text)
    

