import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
#Need to subset by course to find average score per  par 3,4,5 
#split the group into short,avg,long for each section
#Add Categorical Course Attributes to be apply to subset data for precisely for model
holeData = pd.read_excel('HoleData.xlsx')
#Join Course Data all together
courseData = pd.read_excel("course_attributes.xlsx")
courseSchedule = pd.read_excel('courseSchedule.xlsx')
scores = pd.read_excel('dataset2.xlsx')

courseList = holeData["Course"].unique()
years = holeData["Year"].unique()

data = pd.DataFrame(columns=["Year","Course","3SAvg","3SDist","3LAvg","3LDist","4SAvg","4SDist","4LAvg","4LDist","5SAvg","5SDist","5LAvg","5LDist"]) 

print(holeData[holeData["Par"]==3].mean())
##196.87 Yards
print(holeData[holeData["Par"]==4].mean())
##432.36 Yards
print(holeData[holeData["Par"]==5].mean())
##564.09 Yards
pars = [3,4,5]
avgyards= [197, 432, 564]
for c in courseList:
    for y in years:
        temp = holeData[holeData["Course"]==c]
        temp= temp[temp["Year"] == y]
        if temp.empty != True:
            partemp = temp[temp["Par"]==3]
            lower = partemp[partemp["Yardage"]<=avgyards[0]]
            upper = partemp[partemp["Yardage"]>avgyards[0]]
            avg3s = (lower["AverageScore"].mean())
            avg3l = (upper["AverageScore"].mean())
            dist3s = (lower["Yardage"].mean())
            dist3l = (upper["Yardage"].mean())

            partemp = temp[temp["Par"]==4]
            lower = partemp[partemp["Yardage"]<=avgyards[1]]
            upper = partemp[partemp["Yardage"]>avgyards[1]]
            avg4s = (lower["AverageScore"].mean())
            avg4l = (upper["AverageScore"].mean())
            dist4s = (lower["Yardage"].mean())
            dist4l = (upper["Yardage"].mean())

            partemp = temp[temp["Par"]==5]
            lower = partemp[partemp["Yardage"]<=avgyards[2]]
            upper = partemp[partemp["Yardage"]>avgyards[2]]
            avg5s = (lower["AverageScore"].mean())
            avg5l = (upper["AverageScore"].mean())
            dist5s = (lower["Yardage"].mean())
            dist5l = (upper["Yardage"].mean())
            row = {'Year': y, 'Course': c,"3SAvg" : avg3s,"3SDist": dist3s ,"3LAvg": avg3l ,"3LDist": dist3l ,
                   "4SAvg" : avg4s,"4SDist": dist4s ,"4LAvg": avg4l ,"4LDist": dist4l ,
                   "5SAvg" : avg5s,"5SDist": dist5s ,"5LAvg": avg5l ,"5LDist": dist5l }
            data = data.append(row, ignore_index=True) 
#Merge Course Data and Schedule
course = pd.merge(data, courseData, on=['Year','Course'], how='left')
print(course.columns)
course = pd.merge(course, courseSchedule, on=['Year','Course'], how='left')
print(course.dtypes)

def convert_length(length_str):
    # Split the string into value and unit
    if isinstance(length_str, str) == False:
        length_str = str(length_str)
        print(length_str)
    if "'" in length_str and '"' in length_str:
        inch, cent = length_str.split("'")
        inch = inch.replace("'", "")
        cent = cent.replace('"',"")
        inch = float(inch)
        cent = float(cent)* 0.393701
        value = inch + cent
    else:
        value=float(length_str)
    return value

course[['Year', 'Tournament', 'Course']] = course[['Year', 'Tournament', 'Course']].astype(str)
scores[['Year', 'Tournament']] = scores[['Year', 'Tournament']].astype(str)
course.Tournament = course.Tournament.str.replace('\xa0','')

scores['Rough Proximity'] = scores['Rough Proximity'].apply(convert_length)
scores['Average Distance of Putts made'] = scores['Average Distance of Putts made'].apply(convert_length)
scores['Proximity to Hole'] = scores['Proximity to Hole'].apply(convert_length)
scores = pd.merge(scores, course, on=['Year','Tournament'], how='left')

numerical_pipe = SimpleImputer(strategy ="mean")

scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage',  'Scrambling', 
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']] = scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage', 'Scrambling', 
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']].apply(pd.to_numeric, errors='coerce')
numeric_columns = scores.select_dtypes(include = ["number", "integer","float"]).columns
scores[numeric_columns] = numerical_pipe.fit_transform(scores[numeric_columns])
print(scores.columns)
if 'Unnamed: 0' in scores.columns:
    scores = scores.drop('Unnamed: 0', axis=1)
scores.to_excel("CleanedData.xlsx")