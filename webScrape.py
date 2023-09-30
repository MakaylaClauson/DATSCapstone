import requests, openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.select import Select

##URLS for each webpage
URLS = ["https://www.pgatour.com/stats/detail/02428"]
##Class ID for the data needing to be scraped 
ID = ["chakra-text css-dzv7ky","chakra-text css-1osk6s4","chakra-text css-138etjk"]
for x in URLS:
    driver = webdriver.Chrome()
    driver.get(x)
    #Toggle Button for Tournament Only
    l = driver.find_element("class","chakra-menu__menuitem css-fygvng")
    l.click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    players = soup.find('tbody', class_= "css-0").find_all('tr')
    statName = soup.find('h1', class_="chakra-text css-n9y8ye").text
    year = soup.find('p',class_="chakra-text css-1l26nns").text.split('-')[1]
    tournament = soup.find_all('div',class_="css-bq4mok")
    tournament = tournament[2].text.split("Tournament")[1]
    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.append(["Year","Tournament","Name",statName])
    for players in players:
        #What to do with blank rows that break the code 
        name = players.find('span', class_="chakra-text css-1osk6s4").text
        stat = players.find('span', class_="chakra-text css-138etjk").text
        sheet.append([year,tournament, name, stat])
        excel.save(tournament+year+statName+'.csv')

    

