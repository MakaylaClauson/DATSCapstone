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
from selenium.webdriver.chrome.options import Options

URLS = ["https://www.pgatour.com/stats/detail/02428"
        ,"https://www.pgatour.com/stats/detail/102"
        ,"https://www.pgatour.com/stats/detail/101"
        ,"https://www.pgatour.com/stats/detail/103","https://www.pgatour.com/stats/detail/331",
        "https://www.pgatour.com/stats/detail/437","https://www.pgatour.com/stats/detail/130",
        "https://www.pgatour.com/stats/detail/438","https://www.pgatour.com/stats/detail/120",
        "https://www.pgatour.com/stats/detail/142","https://www.pgatour.com/stats/detail/143",
        "https://www.pgatour.com/stats/detail/144"]

data = pd.DataFrame(columns = ["Year", "Tournament","Course", "Name"])

courseSchedule = pd.read_excel("courseSchedule.xlsx")
print(courseSchedule)
courseSchedule.Tournament = courseSchedule.Tournament.str.replace('\xa0','')

# Convert the DataFrame to a dictionary of dictionaries
dict = {}

for i in range(courseSchedule.shape[0]):
    row_dict = {}
    for col in courseSchedule.columns:
        row_dict[col] = courseSchedule.loc[i, col]
    dict[i] = row_dict

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
                data = pd.merge(data, t, on=['Year','Tournament','Name','Course'], how='inner')
            else:
                data = data.append(t,ignore_index=True)
        else:
            data = data.append(t,ignore_index=True)
    else:
        data = data.append(t,ignore_index=True)

def scrape():
    global dict
    for x in URLS:
        temp = pd.DataFrame(columns = ["Year", "Tournament", "Name"]) 
        options = Options()
        options.add_argument("--headless")
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome()
        driver.get(x)
        for value in dict.values():
            years = value['Year']
            tournaments = value['Tournament']
            course = value['Course']
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
                row = {'Year': year, 'Tournament': tournament,'Course': course, 'Name': name, statName: stat}
                temp = temp.append(row, ignore_index=True) 
    print(temp)
    dataset(temp,tournaments, year,statName)


scrape()
data.to_excel("finaldataset.xlsx",index=False)