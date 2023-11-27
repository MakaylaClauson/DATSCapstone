import pandas as pd
import numpy as np
import shap
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import  DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import RFECV
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
import seaborn as sns
# Modelling


scores = pd.read_excel('CleanedData.xlsx')

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
    rfe = E(rf,cv=5,scoring="neg_mean_squared_error")
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
def feature_sel():
    features = scores[['Total Putting', 'Driving Accuracy Percentage', 'Driving Distance',
                'Greens in Regulation Percentage', 'Proximity to Hole',
                'Rough Proximity', 'Scrambling', 'Average Distance of Putts made',
                'Par 3 Scoring Average', 'Par 4 Scoring Average', 'Par 5 Scoring Average'
                ,"3SAvg","3SDist","3LAvg","3LDist","4SAvg","4SDist","4LAvg","4LDist","5SAvg","5SDist","5LAvg","5LDist"]]
    target = scores['Scoring Average']
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    # Create a decision tree classifier and train it
    model = RandomForestRegressor()
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    results = permutation_importance(
        model, X_test, y_test, n_repeats = 10, random_state=42, n_jobs = -10
    )
    sorted_importance = results.importances_mean.argsort()
    importances = pd.DataFrame(results.importances[sorted_importance].T,
                            columns= scores.columns[sorted_importance])

    sns.set(style="whitegrid")
    sns.set_context("notebook", rc={"lines.linewidth": 2.5})
    num_columns = len(importances.columns)

    # Set the number of subplots to show at a time
    subplots_per_figure = 2

    # Calculate the number of figures needed
    num_figures = (num_columns + subplots_per_figure - 1) // subplots_per_figure

    # Iterate over figures
    for fig_num in range(num_figures):
        # Calculate the start and end indices for the current subset of columns
        start_index = fig_num * subplots_per_figure
        end_index = min((fig_num + 1) * subplots_per_figure, num_columns)

        # Create a figure with subplots
        fig, axes = plt.subplots(nrows=1, ncols=end_index - start_index, figsize=(15, 5))

        # Iterate through the subset of columns and create violin plots using Seaborn
        for i, (column, data) in enumerate(importances.iloc[:, start_index:end_index].iteritems()):
            sns.violinplot(data=data, ax=axes[i])
            axes[i].set_title(column)
            axes[i].set_ylabel('Importance')

        plt.tight_layout()
        plt.show()
#feature_sel()

def feature_import(target_golfer):
    if target_golfer == "none":
        subset_df = scores
    else:
        subset_df = scores[scores['Name'] == target_golfer]
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
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)
    # Create a decision tree classifier and train it
    model = RandomForestRegressor()
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    explainer = shap.Explainer(model)
    shap_values = explainer.shap_values(X_test)

    # Summarize feature importances
    shap.summary_plot(shap_values, X_test)
    shap.dependence_plot("Driving Distance", shap_values, X_test, interaction_index = "5LAvg")
    shap.decision_plot(explainer.expected_value, shap_values, X_test.columns)
feature_import("none")
