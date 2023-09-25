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

        #import into pandas dataframe
print(data)
    #export as CSV File with correct naming -- FInd YEar TOurnament Stat in HTML -- SET Stat name as chosen abbrev. 
    #Year retive first 4 digits

