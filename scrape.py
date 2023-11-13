import requests, openpyxl
from bs4 import BeautifulSoup
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re
from selenium.webdriver.chrome.options import Options


##URLS for each webpage
URLS = ["https://www.pgatour.com/stats/detail/02428"
        ,"https://www.pgatour.com/stats/detail/102"
        ,"https://www.pgatour.com/stats/detail/101"
        ,"https://www.pgatour.com/stats/detail/103","https://www.pgatour.com/stats/detail/331",
        "https://www.pgatour.com/stats/detail/437","https://www.pgatour.com/stats/detail/130",
        "https://www.pgatour.com/stats/detail/438","https://www.pgatour.com/stats/detail/120",
        "https://www.pgatour.com/stats/detail/142","https://www.pgatour.com/stats/detail/143",
        "https://www.pgatour.com/stats/detail/144"]
##Class ID for the data needing to be scraped 
ID = ["chakra-text css-dzv7ky","chakra-text css-1osk6s4","chakra-text css-138etjk"]
TS = ["TOUR Championship","The Open Championship","U.S. Open", 
      "PGA Championship","Masters Tournament","THE PLAYERS Championship"]
YS = ["2022-2023","2021-2022"
      ,"2020-2021","2019-2020","2018-2019","2017-2018","2016-2017"
      ,"2015-2016","2014-2015","2013-2014"]
data = pd.DataFrame(columns = ["Year", "Tournament", "Name"])
temp2 = pd.DataFrame(columns = ["Year","Tournament", "Course"]) 

def safe_text(element):
    if element is not None:
        return element.text
    else:
        return ""
    
def find_element_safely(driver, by, value):
    try:
        element = driver.find_element(by, value)
        return element
    except NoSuchElementException:
        return False
    
def dataset(t,tour, y,sn):
    global data
    t = t[(t['Name'] != '')]
    t = t.reset_index(drop=True)
    t[sn] = t[sn].str.replace('%', '', regex=False)
    if data.empty != True:
        if data.isin([tour]).any().any():
            if data.isin([y]).any().any():
                data = pd.merge(data, t, on=['Year','Tournament','Name'], how='inner')
            else:
                data = data.append(t,ignore_index=True)
        else:
            data = data.append(t,ignore_index=True)
    else:
        data = data.append(t,ignore_index=True)
    
    #if statement if name, year, tournament match add new statName column else append to dataframe 


def scrape(): 
    global data  
    for x in URLS:
        #Toggle Button for Tournament Only
        temp = pd.DataFrame(columns = ["Year", "Tournament", "Name"]) 
        for tournaments in TS:
            for years in YS:
                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
                driver.get(x)
                y = driver.find_element(By.XPATH, '//*[contains(text(), "Season")]')
                driver.execute_script("arguments[0].click();", y)
                xpath =  f'//button[@role="menuitem" and contains(text(), "{years}")]'
                sy = o = find_element_safely(driver, By.XPATH, xpath)
                if sy == False:
                    continue 
                driver.execute_script("arguments[0].click();", sy)
                sleep(5)
                t = driver.find_element(By.XPATH, '//*[contains(text(), "Tournament")]')
                driver.execute_script("arguments[0].click();", t)
                sleep(5)
                tpath = f'//button[@role="menuitem" and contains(text(), "{tournaments}")]'
                ty = o = find_element_safely(driver, By.XPATH, tpath)
                if ty == False:
                    continue 
                tn = driver.find_element(By.XPATH, tpath)
                driver.execute_script("arguments[0].click();", tn)
                sleep(5)
                p_element = driver.find_element(By.XPATH, '//*[contains(text(), "Time Period")]')
                driver.execute_script("arguments[0].click();", p_element)
                to = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(), "Tournament Only")]')
                driver.execute_script("arguments[0].click();", to)
                sleep(5)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html5lib')
                year = soup.find('p',class_="chakra-text css-1e5ks3").text
                year = year.split('-')[1]
                players = soup.find('tbody', class_= "css-0")
                statName = soup.find('h1', class_="chakra-text css-n9y8ye").text
                tournament = soup.find('p', class_="chakra-text css-9ibfze").text
                tournament = tournament.split(",")[0]
                for players in players:
                    name = safe_text(players.find('span', class_="chakra-text css-1osk6s4"))
                    stat = safe_text(players.find('span', class_="chakra-text css-138etjk"))
                    if stat == "":
                        stat = safe_text(players.find('span', class_="chakra-text css-q5ejb6"))
                        if stat == "":
                            stat = safe_text(players.find('span', class_="chakra-text css-yiy6zj"))
                    row = {'Year': year, 'Tournament': tournament, 'Name': name, statName: stat}
                    temp = temp.append(row, ignore_index=True) 
                driver.close()
        dataset(temp,tournaments, year,statName)



def courseScrape():
    global temp2
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.pgatour.com/schedule")
    #Toggle Button for Tournament Only
    p_element = driver.find_element(By.XPATH, '//*[contains(text(), "View")]')
    driver.execute_script("arguments[0].click();", p_element)
    to = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(), "Full Schedule")]')
    driver.execute_script("arguments[0].click();", to)
    sleep(5) 
    for years in YS:
        y = driver.find_element(By.XPATH, '//*[contains(text(), "Season")]')
        driver.execute_script("arguments[0].click();", y)
        xpath =  f'//button[@role="menuitem" and contains(text(), "{years}")]'
        sy = o = find_element_safely(driver, By.XPATH, xpath)
        if sy == False:
            continue 
        driver.execute_script("arguments[0].click();", sy)
        sleep(30)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html5lib')
        year = safe_text(soup.find('p',class_="chakra-text css-1l26nns"))
        if year != "":
            year = year.split('-')[1]
        courses = soup.find_all('div', class_= "css-j7qwjs")
        for course in courses:
            tournament = safe_text(course.find('p', class_="chakra-text css-vgdvwe"))
            tournament = re.sub(r'\([^)]*\)', '', tournament)
            course = safe_text(course.find('p', class_="chakra-text css-16dpohb"))
            row = {'Year': year, 'Tournament': tournament, 'Course': course}
            temp2 = temp2.append(row, ignore_index=True) 
        print(temp2)

#scrape()
courseScrape()
print(data)
#data.to_excel("dataset2.xlsx",index=False)
temp2.to_excel("courseSchedule.xlsx",index=False)