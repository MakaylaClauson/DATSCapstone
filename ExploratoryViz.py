import pandas as pd 
import seaborn as sns
import requests, openpyxl
import matplotlib.pyplot as plt
import numpy as np

scores = pd.read_excel('dataset2.xlsx')
course = pd.read_excel('PGACourseData.xlsx')

course[['Year', 'Tournament', 'Course']] = course[['Year', 'Tournament', 'Course']].astype(str)
scores[['Year', 'Tournament']] = scores[['Year', 'Tournament']].astype(str)
course.Tournament = course.Tournament.str.replace('\xa0','')

df = pd.read_excel('CleanedData.xlsx')
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1)


def course_graph():
    plt.figure(figsize=(15, 6))  # Adjust the figure size as needed
    plt.scatter(course['Yardage'], course['AverageScore'], color='skyblue', marker='o')
    z = np.polyfit(course['Yardage'], course['AverageScore'], 1)
    p = np.poly1d(z)
    plt.plot(course['Yardage'], p(course['Yardage']), color='red', label='Best Fit Line')
    
    plt.xlabel('Course Yardage')
    plt.ylabel('Average Score')  # Adjust the ylabel as needed
    plt.title('Scatter Plot of Course Yardage vs. Average Score')
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.show()

#course_graph()

def corr_matrix(target_golfer):
    data = df[df['Name'] == target_golfer]
    correlation_matrix = data.corr()

    # Filter the correlation matrix to include only values above 0.5 or below -0.5
    high_corr_matrix = correlation_matrix[(correlation_matrix.abs() > 0.5) & (correlation_matrix != 1)]
    for i in high_corr_matrix.index:
        for j in high_corr_matrix.columns:
            if pd.isna(high_corr_matrix.loc[i, j]):
                high_corr_matrix.loc[i, j] = ''
            else:
                high_corr_matrix.loc[i, j] = f'{high_corr_matrix.loc[i, j]:.3g}'
    annot_font_size = 6
    # Visualize the correlation matrix using a heatmap with annotated text
    plt.figure(figsize=(10, 10))
    sns.heatmap(correlation_matrix, annot=high_corr_matrix, cmap='coolwarm', linewidths=.5,fmt='',annot_kws={'size': annot_font_size})
    plt.title(f'Correlation Matrix (Values above 0.5 or below -0.5) for {target_golfer}')
    plt.show()

corr_matrix("Rory McIlroy")