import pandas as pd
import numpy as np
import sys
from pathlib import Path
import os 

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


def read_roster(path = "utils/students.csv"):
    return pd.read_csv(path)

def candidate_teams(df, num_teams = 5):
    df_ = df.copy()
    team_size = len(df_) // num_teams + 1
    group_nums = np.tile(np.arange(num_teams), team_size)[:len(df_)]
    np.random.shuffle(group_nums)
    df_["team"] = group_nums

    return df_

def check_teams(df): 
    df_ = df.copy()
    df_["is_f"] = df_["gender"] == "F"
    grouped = df_.groupby("team")["is_f"].sum()
    df_ = df_.drop("is_f", axis = 1)
    return not (1 in grouped.values)
    
def assign_teams(df, num_teams = 5):
    df_ = candidate_teams(df, num_teams = num_teams)
    while not check_teams(df_):
        df_ = candidate_teams(df, num_teams = num_teams)
    return df_    

def reset_presentation(df):
    """
    need to check for correct behavior on this
    """
    df_ = df.copy()
    if "presented" not in df.columns: 
        df_["presented"] = False
    df_["all_presented"] = df_.groupby(["section", "team"])["presented"].transform(np.all)
    with pd.option_context('mode.chained_assignment', None):
        df_["presented"][df_["all_presented"]] = False
    df_ = df_.drop("all_presented", axis = 1)
    return df_
    
def shuffle(df):
    df_ = df.copy()
    df_ = reset_presentation(df_)
    df_["r"] = np.random.rand(len(df_))
    df_ = df_.sort_values(by = ["section", "team", "presented", "r"])
    min_r = df_.groupby(["section", "team", "presented"])["r"].transform(min)
    ix = np.isclose(df_["r"], min_r)
    df_.loc[ix, "presented"] = True
    df_ = df_.drop("r", axis = 1)
    
    display_teams(df)
    
    return df_

def display_teams(df, section = "A"):
    console = Console()
    panels = []
    
    df_section = df[df["section"] == section].copy()
    
    teams = np.unique(df.team)
    
    for team in teams: 
        panel_str = ""
        df_ = df[df["team"] == team]
        for i in range(len(df_)):
            
            # if i == 0:    
            #     print('\033[1m' + "\033[94m")
            
            first = df_["first"].iloc[i]
            last = df_["last"].iloc[i]    
            panel_str += format_student(first, last, i) + "\n"
            
        panels.append(Panel(panel_str))

    console.print(Columns(panels))
    
def format_student(first, last, i):
    # https://rich.readthedocs.io/en/stable/markup.html
    if i == 0:
        return f":bulb:[b green]{first} {last}[/]"
    return f"  {first} {last}"

 
if __name__ == "__main__":
    if sys.argv[1] == "init":
        df = read_roster()
        df = assign_teams(df, num_teams = 5)
        df.to_csv("utils/teams.csv", index = False)
    elif sys.argv[1] == "teams":
        df = pd.read_csv("utils/teams.csv")
        df = assign_teams(df, num_teams = 5)
        df.to_csv("utils/teams.csv", index = False)
    elif sys.argv[1] == "shuffle":
        df = pd.read_csv("utils/teams.csv")
        df = shuffle(df)
        df.to_csv("utils/teams.csv", index = False)
