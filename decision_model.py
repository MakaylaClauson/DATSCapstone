import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import  DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import RFECV
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
# Modelling


scores = pd.read_excel('dataset2.xlsx')
course = pd.read_excel('PGACourseData.xlsx')

course[['Year', 'Tournament', 'Course']] = course[['Year', 'Tournament', 'Course']].astype(str)
scores[['Year', 'Tournament']] = scores[['Year', 'Tournament']].astype(str)
course.Tournament = course.Tournament.str.replace('\xa0','')

#print(course)
#course.to_excel("CourseData.xlsx",index=False)

#Join Course Data and Player Data -- Research better Course Data 
#data = pd.merge(scores, course,on=['Year','Tournament'], how = 'left')
#print(data)
#data.to_excel('PGA5_Dataset.xlsx')

#Inches/Centimeters Converter
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

def indv_model(name):
    print(name)
    #subset_df = scores[scores['Name'] == name]
    subset_df = scores
    print(subset_df)
    features = subset_df[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage', 'Proximity to Hole',
               'Rough Proximity', 'Scrambling', 'Average Distance of Putts made',
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average'
               ,"3SAvg","3SDist","3LAvg","3LDist","4SAvg","4SDist","4LAvg","4LDist","5SAvg","5SDist","5LAvg","5LDist"]]
    target = subset_df['Scoring Average']
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    # Create a decision tree classifier and train it
    rf = RandomForestRegressor()
    rf.fit(X_train,y_train)
    y_pred = rf.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("Predicted Values", X_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")
    rfe = RFECV(rf,cv=5,scoring="neg_mean_squared_error")
    rfe.fit(X_train, y_train)
    selected_features = np.array(features)[rfe.get_support()]
    print(selected_features)
    #Display Model
    f_i = list(zip(features,rf.feature_importances_))
    f_i.sort(key = lambda x : x[1])
    plt.barh([x[0] for x in f_i],[x[1] for x in f_i])
    plt.show()

def anothermodel():
    subset_df = scores
    print(subset_df)
    features = subset_df[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage', 'Proximity to Hole',
               'Rough Proximity', 'Scrambling', 'Average Distance of Putts made',
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average'
               ,"3SAvg","3SDist","3LAvg","3LDist","4SAvg","4SDist","4LAvg","4LDist","5SAvg","5SDist","5LAvg","5LDist"]]
    target = subset_df['Scoring Average']
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    # Create a decision tree classifier and train it
    model = RandomForestRegressor()
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    print(f"model score on training data: {model.score(X_train, y_train)}")
    print(f"model score on testing data: {model.score(X_test, y_test)}")
    importances = model.feature_importances_
    print(importances)
    print(y_test, y_pred)

    
#Label Encoding
label_encoder = LabelEncoder()
#scores['Name'] = label_encoder.fit_transform(scores['Name'])
#scores['Tournament'] = label_encoder.fit_transform(scores['Tournament'])

# Fit and transform the data

scores['Rough Proximity'] = scores['Rough Proximity'].apply(convert_length)
scores['Average Distance of Putts made'] = scores['Average Distance of Putts made'].apply(convert_length)
scores['Proximity to Hole'] = scores['Proximity to Hole'].apply(convert_length)
scores = pd.merge(scores, course, on=['Year','Tournament'], how='left')

scores = scores.dropna()

scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage',  'Scrambling', 
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']] = scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage', 'Scrambling', 
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']].apply(pd.to_numeric, errors='coerce')
#print(scores)
#nan_count_per_column = scores.isna().sum()
#print("Number of NaN values per column:")
#print(nan_count_per_column)

#indv_model("Rory McIlroy")
anothermodel()


##Find propability that they will par each type of hole 