import requests 
from bs4 import BeautifulSoup
import pandas as pd
#import Selenium 


##Find Class names
#Extract URLS from website for link in soup.find_all('a'):
    ##print(link.get('href'))
##URLS for each webpage
URLS = ["https://www.pgatour.com/stats/detail/02428"]
##Class ID for the data needing to be scraped 
ID = ["chakra-text css-dzv7ky","chakra-text css-1osk6s4","chakra-text css-138etjk"]
for x in URLS:
<<<<<<< Updated upstream
    page = requests.get(x)
    soup = BeautifulSoup(page.content, 'html5lib')
    table = soup.find('tbody', attrs = {'id':'css-0'}) 
    print(table)
    #Name Tournament Course? Statistic -- have to find Statistic Name in HTML
    data = pd.DataFrame()
    for z in ID:
        print(z)
        for row in table.findAll('div', attrs = {'class':z}):
            print(row)
            data = data.append(row,ignore_index=True)
=======
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
            excel = openpyxl.Workbook()
            sheet = excel.active
            sheet.append(["Year","Tournament","Name",statName])
            for players in players:
        #What to do with blank rows that break the code 
                #add function to determine if there is a blank row 
                print(players)
                blank_line()
                name = players.find('span', class_="chakra-text css-1osk6s4").text
                stat = players.find('span', class_="chakra-text css-138etjk").text
                sheet.append([year,tournament, name, stat])
                excel.save(tournament+year+statName+'.csv')
>>>>>>> Stashed changes

        #import into pandas dataframe
print(data)
    #export as CSV File with correct naming -- FInd YEar TOurnament Stat in HTML -- SET Stat name as chosen abbrev. 
    #Year retive first 4 digits

def blank_line():
    if :
    
    return 