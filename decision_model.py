import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

scores = pd.read_excel('dataset2.xlsx')
courseSchedule = pd.read_excel('courseSchedule.xlsx')
#courseData = pd.read_csv('CourseTable.csv')
#Need to subset by course to find average score per  par 3,4,5 
holeData = pd.read_excel('HoleData.xlsx')
#Join Course Data all together
courseData = pd.read_excel("course_attributes.xlsx")

#Merge Course Data and Schedule
course = pd.merge(courseSchedule, courseData, left_on='Course', right_on='COURSE')
del course['COURSE']
print(course.dtypes)
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
    subset_df = scores[scores['Name'] == name]
    print(subset_df)
    features = subset_df[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage', 'Proximity to Hole',
               'Rough Proximity', 'Scrambling', 'Average Distance of Putts made',
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']]
    target = subset_df['Scoring Average']
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    # Create a decision tree classifier and train it
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print("Predicted Values", X_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared: {r2:.2f}")
    #Display Model
    plt.figure(figsize=(12, 8))
    plot_tree(model, feature_names=X_train.columns, filled=True, rounded=True)
    plt.show()

#Label Encoding
label_encoder = LabelEncoder()
#scores['Name'] = label_encoder.fit_transform(scores['Name'])
#scores['Tournament'] = label_encoder.fit_transform(scores['Tournament'])

# Fit and transform the data
scores = scores.dropna()

scores['Rough Proximity'] = scores['Rough Proximity'].apply(convert_length)
scores['Average Distance of Putts made'] = scores['Average Distance of Putts made'].apply(convert_length)
scores['Proximity to Hole'] = scores['Proximity to Hole'].apply(convert_length)

scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage',  'Scrambling', 
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']] = scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
               'Greens in Regulation Percentage', 'Scrambling', 
               'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average']].apply(pd.to_numeric, errors='coerce')
print(scores)
nan_count_per_column = scores.isna().sum()
print("Number of NaN values per column:")
print(nan_count_per_column)

indv_model("Rory McIlroy")


