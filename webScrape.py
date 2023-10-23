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
<<<<<<< Updated upstream
TS = ["TOUR Championship"]
YS = ["2021-2022"]
for x in URLS:
=======
TS = ["TOUR Championship","BMW Championship","Sanderson Farms Championship",
      "Fortinet Championship","FedEx St. Jude Championship","Wyndham Championship",
      "3M Open","The Open Championship","Genesis Scottish Open","Barbasol Championship",
      "John Deere Classic,Rocket Mortgage Classic","Travelers Championship","U.S. Open", 
      "RBC Canadian Open", "the Memorial Tournament", "Charles Schwab Challenge", 
      "PGA Championship", "AT&T Byron Nelson","Wells Fargo Championship","Mexico Open "
      ,"RBC Heritage","Masters Tournament","Valero Texas Open", "Corales Puntacana Championship"
      , "Valspar Championship","THE PLAYERS Championship", "Puerto Rico Open"
      ,"Arnold Palmer Invitational ", "The Honda Classic", "The Genesis Invitational",
      "WM Phoenix Open", "AT&T Pebble Beach ", "Farmers Insurance Open", "The American Express", 
     "Sony Open in Hawaii", "Sentry Tournament of Champions", "THE CJ CUP in South Carolina", "ZOZO CHAMPIONSHIP"
      , "The RSM Classic", "Cadence Bank Houston Open","World Wide Technology Championship","Butterfield Bermuda Championship"]
YS = ["2022-2023","2021-2022"
      ,"2020-2021","2019-2020","2018-2019","2017-2018","2016-2017"
      ,"2015-2016","2014-2015","2013-2014"]
data = pd.DataFrame(columns = ["Year", "Tournament", "Name"])

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
    for x in URLS:
        driver = webdriver.Chrome()
        driver.get(x)
        #Toggle Button for Tournament Only
        p_element = driver.find_element(By.XPATH, '//*[contains(text(), "Time Period")]')
        driver.execute_script("arguments[0].click();", p_element)
        to = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(), "Tournament Only")]')
        driver.execute_script("arguments[0].click();", to)
        sleep(5)
        temp = pd.DataFrame(columns = ["Year", "Tournament", "Name"]) 
        for tournaments in TS:
            for years in YS:
                y = driver.find_element(By.XPATH, '//*[contains(text(), "Season")]')
                driver.execute_script("arguments[0].click();", y)
                xpath =  f'//button[@role="menuitem" and contains(text(), "{years}")]'
                sy = o = find_element_safely(driver, By.XPATH, xpath)
                if sy == False:
                    continue 
                driver.execute_script("arguments[0].click();", sy)
                sleep(10)
                t = driver.find_element(By.XPATH, '//*[contains(text(), "Tournament")]')
                driver.execute_script("arguments[0].click();", t)
                tpath = f'//button[@role="menuitem" and contains(text(),"{tournaments}")]'
                tn = find_element_safely(driver, By.XPATH, tpath)
                if tn == False:
                    continue 
                driver.execute_script("arguments[0].click();", tn)
                sleep(10)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html5lib')
                year = safe_text(soup.find('p',class_="chakra-text css-1l26nns"))
                if year != "":
                    year = year.split('-')[1]
                else:
                    continue
                players = safe_text(soup.find('tbody', class_= "css-0"))
                if players != "":
                    soup.find('tbody', class_= "css-0").find_all('tr')
                else:
                    continue 
                statName = safe_text(soup.find('h1', class_="chakra-text css-n9y8ye"))
                tournament = soup.find_all('div',class_="css-bq4mok")
                tournament = safe_text(tournament[2])
                if tournament != "":
                    tournament = tournament.split("Tournament")[1]
                else:
                    continue
                for players in players:
                    name = safe_text(players.find('span', class_="chakra-text css-1osk6s4"))
                    stat = safe_text(players.find('span', class_="chakra-text css-138etjk"))
                    if stat == "":
                        stat = safe_text(players.find('span', class_="chakra-text css-q5ejb6"))
                        if stat == "":
                            stat = safe_text(players.find('span', class_="chakra-text css-yiy6zj"))
                    row = {'Year': year, 'Tournament': tournament, 'Name': name, statName: stat}
                    temp = temp.append(row, ignore_index=True) 
        dataset(temp,tournament, year,statName)
def courseScrape():
    global data
>>>>>>> Stashed changes
    driver = webdriver.Chrome()
    driver.get(x)
    #Toggle Button for Tournament Only
    p_element = driver.find_element(By.XPATH, '//*[contains(text(), "Time Period")]')
    driver.execute_script("arguments[0].click();", p_element)
    to = driver.find_element(By.XPATH, '//button[@role="menuitem" and contains(text(), "Tournament Only")]')
    driver.execute_script("arguments[0].click();", to)
<<<<<<< Updated upstream
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
            excel = openpyxl.Workbook()
            sheet = excel.active
            sheet.append(["Year","Tournament","Name",statName])
            for players in players:
        #What to do with blank rows that break the code 
                print(players)
                name = players.find('span', class_="chakra-text css-1osk6s4").text
                stat = players.find('span', class_="chakra-text css-138etjk").text
                sheet.append([year,tournament, name, stat])
                excel.save(tournament+year+statName+'.csv')


=======
    sleep(5) 
    temp2 = pd.DataFrame(columns = ["Year","Tournament", "Course"]) 
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
            course = safe_text(course.find('p', class_="chakra-text css-16dpohb"))
            row = {'Year': year, 'Tournament': tournament, 'Course': course}
            temp2 = temp2.append(row, ignore_index=True) 
        print(temp2)
    temp2.to_excel("coursespga.xlsx",index=False)
    data = pd.merge(data, temp2, on=['Year','Tournament'], how='left')

scrape()
courseScrape()
print(data)
data.to_excel("pgadata2.xlsx",index=False)
>>>>>>> Stashed changes
