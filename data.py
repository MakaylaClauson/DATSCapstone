import os
import pandas as pd

#Set File Path
filepath = "/Users/makaylaclauson/Documents/DATS4001/TournamentData"
os.chdir(filepath)

#Load Tournament Scoring Data for Past 10 Years 
years = ["2023"]
tournaments = ["Tour Championship"]
stats = ["","Driving Distance","Driving Accuracy","GIR","FTG","RTG","PuttDist","Putts","PAR3","PAR4","PAR5","ScramblingGreen"]

d = pd.DataFrame()
temp = pd.DataFrame()
for x in years:
   for y in tournaments:
        for z in stats:
                temp = pd.read_csv(y+x+z+'.csv')
                temp['Year'] = x
                temp['Tournament'] = y
                temp = temp.drop(['RANK','MOVEMENT','PLAYER'],axis=1)
                temp.rename(columns = {'AVG':'AVG'+z}, inplace = True)
                temp.rename(columns = {'%':'%'+z}, inplace = True)
                temp.rename(columns = {'TOTAL STROKES':'TOTAL STROKES '+z}, inplace = True)
                temp.rename(columns = {'TOTAL HOLES':'TOTAL HOLES '+z}, inplace = True)
                if z == "":
                        d = d.append(temp)
                else:
                        d = pd.merge(d, temp, on=['Year','Tournament','PLAYER_ID'], how='inner')

coursetable = pd.read_csv('CourseTable.csv')
d=pd.merge(d,coursetable, on='COURSE', how='left')
print(d.head())
d.to_excel('mydata.xlsx')
