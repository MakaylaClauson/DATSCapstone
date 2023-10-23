import pandas as pd 
import seaborn as sns
import requests, openpyxl
import matplotlib.pyplot as plt

df = pd.read_excel('pgadata.xlsx')


def score_graph(tournament):
    filtered_df = df[df['Tournament'] == tournament]
    golfer_counts = filtered_df['Name'].value_counts()
    print(golfer_counts)
    selected_golfers = golfer_counts[golfer_counts >= 5].index
    print(selected_golfers)
    filtered_df = filtered_df[filtered_df['Name'].isin(selected_golfers)]
    print(filtered_df)

    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    graph = sns.relplot(x="Year", y="Scoring Average", data=filtered_df, hue="Name", kind = "line")
    graph.set_titles("Scores Over Years by {tournament}")
    graph.set_axis_labels("Year", "Scoring Average")
    #graph.fig.suptitle("Scoring Average Over Years by Tournament for Each Player")
    plt.show()

score_graph("U.S. Open")