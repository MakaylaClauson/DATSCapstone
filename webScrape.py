import requests, openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

##URLS for each webpage
URLS = ["https://www.pgatour.com/stats/detail/02428"]
##Class ID for the data needing to be scraped 
ID = ["chakra-text css-dzv7ky","chakra-text css-1osk6s4","chakra-text css-138etjk"]
TS = ["TOUR Championship"]
YS = ["2021-2022"]
data = pd.DataFrame(columns = ["Year", "Tournament", "Name"])

def safe_text(element):
    if element is not None:
        return element.text
    else:
        return ""
    
def dataset(t,tour, y,sn):
    global data
    t = t[(t['Name'] != '')]
    t = t.reset_index(drop=True)
    if data.empty != True:
        if data.isin([tour]).any().any():
            if data.isin([y]).any().any():
                data[sn] = t[sn]
        else:
            data = data.append(t,ignore_index=True)
    else:
        data = data.append(t,ignore_index=True)
    
    #if statement if name, year, tournament match add new statName column else append to dataframe 


def scrape():   
    for x in URLS:
        driver = webdriver.Chrome()
        driver.get(x)
        #Toggle Button for Tournament Only
        p_element = driver.find_element(By.XPATH, '//*[contains(text(), "Time Period")]')
        driver.execute_script("arguments[0].click();", p_element)
        to = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(), "Tournament Only")]')
        driver.execute_script("arguments[0].click();", to)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Sep 17")]'))) 
        for tournaments in TS:
            t = driver.find_element(By.XPATH, '//*[contains(text(), "Tournament")]')
            driver.execute_script("arguments[0].click();", t)
            tn = o = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(),"TOUR Championship")]')
            driver.execute_script("arguments[0].click();", tn)
            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Aug 27")]'))) 
            for years in YS:
                y = driver.find_element(By.XPATH, '//*[contains(text(), "Season")]')
                driver.execute_script("arguments[0].click();", y)
                sy = o = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(),"2021-2022")]')
                driver.execute_script("arguments[0].click();", sy)
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Aug 28")]'))) 
                html = driver.page_source
                soup = BeautifulSoup(html, 'html5lib')
                year = soup.find('p',class_="chakra-text css-1l26nns").text.split('-')[1]
                players = soup.find('tbody', class_= "css-0").find_all('tr')
                statName = soup.find('h1', class_="chakra-text css-n9y8ye").text
                tournament = soup.find_all('div',class_="css-bq4mok")
                tournament = tournament[2].text.split("Tournament")[1]
                temp = pd.DataFrame(columns = ["Year", "Tournament", "Name"]) 
                for players in players:
                    name = safe_text(players.find('span', class_="chakra-text css-1osk6s4"))
                    stat = safe_text(players.find('span', class_="chakra-text css-138etjk"))
                    row = {'Year': year, 'Tournament': tournament, 'Name': name, statName: stat}
                    temp = temp.append(row, ignore_index=True) 
                dataset(temp,tournament, year,statName)
               
scrape()
