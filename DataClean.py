import pandas as pd
#Need to subset by course to find average score per  par 3,4,5 
#split the group into short,avg,long for each section
#Add Categorical Course Attributes to be apply to subset data for precisely for model
holeData = pd.read_excel('HoleData.xlsx')
#Join Course Data all together
courseData = pd.read_excel("course_attributes.xlsx")
courseSchedule = pd.read_excel('courseSchedule.xlsx')

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
#course.to_excel('PGACourseData.xlsx')

#del course['COURSE']
#print(course.dtypes)
#print(course)
#course.to_excel("CourseData.xlsx",index=False)

#Join Course Data and Player Data -- Research better Course Data 
#data = pd.merge(scores, course,on=['Year','Tournament'], how = 'left')
#print(data)
#data.to_excel('PGA5_Dataset.xlsx')