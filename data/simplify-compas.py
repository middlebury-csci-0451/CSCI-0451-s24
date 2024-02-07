import pandas as pd
df = pd.read_csv("data/compas-scores-two-years.csv")

df["y_pred"] = 1*(df["score_text"] != "Low")
df["y"] = df["two_year_recid"]

df[["y", "y_pred"]].to_csv("data/toy-classification-data.csv", index = False)