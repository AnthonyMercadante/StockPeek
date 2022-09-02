from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

df = pd.DataFrame(columns=['Company', 'Price']) # Creates master data frame

driver = webdriver.Chrome('/Users/raethexn/Documents/GitHub/DataScience/index.html') # Initalize WebDriver
driver.get('https://ca.finance.yahoo.com/quote/') # Open website for scraping

companies = driver.find_elements_by_xpath('//h1@class="D(ib) Fz(18px)"]') # Grab company name
companies_list = [] # Adding company names to list

for c in range(len(companies)): # 
    companies_list.append(companies[c].text)

prices = driver.find_elements_by_xpath('//div[@class="Fw(b) Fz(36px) Mb(-4px) D(ib)"]') # Grab price of company
prices_list = [] # Adding price to list

for p in range(len(prices)):
    prices_list.append(prices_list[p].text)

data_tuples = list(zip(companies_list[1:], prices_list[1:])) # List of each company name and current price
temp_df = pd.DataFrame(data_tuples, columns='Company')# Creates data frame for each tuple in list
df = df.append(temp_df) # appends to master dataframe

driver.close()