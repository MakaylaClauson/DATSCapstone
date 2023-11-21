import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import re

scores = pd.read_excel('dataset2.xlsx')
course = pd.read_excel('PGACourseData.xlsx')

course[['Year', 'Tournament', 'Course']] = course[['Year', 'Tournament', 'Course']].astype(str)
scores[['Year', 'Tournament']] = scores[['Year', 'Tournament']].astype(str)
course.Tournament = course.Tournament.str.replace('\xa0','')
course.Tournament = course.Tournament.str.encode('utf-8')
scores.Tournament = scores.Tournament.str.encode('utf-8')
print(course.Tournament)
print(scores.Tournament)
