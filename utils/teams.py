import pandas as pd
import numpy as np
import sys
from pathlib import Path
import os 

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel

def format_student(name, i):
    # https://rich.readthedocs.io/en/stable/markup.html
    last_first = name.split(", ")
    if i == 0:
        return f":bulb:[b blue]{last_first[1]} {last_first[0]}[/]"
    return f"  {last_first[1]} {last_first[0]}"

def assign_ids():
    A = "CSCI 0451A (Spring 2023)"
    B = "CSCI 0451B (Spring 2023)"

    roster = pd.read_csv("utils/roster.csv")
    
    roster["ix"] = roster.groupby("Section")["Section"].transform(lambda x: np.arange(len(x)))
    
    roster["Section"] = roster["Section"].apply(lambda x: "A_" if x == A else "B_")
    
    roster["id"] = roster["Section"] + roster["ix"].astype(str)
    
    roster = roster.sort_values(by = ["Section", "ix"])
    
    roster[["Student", "id"]].to_csv("utils/roster_id.csv", index = False)

def form_teams(num_groups = 5):
    roster = pd.read_csv("utils/roster_id.csv")
    
    roster_A = roster[roster["id"].str[0] == "A"].copy()
    roster_B = roster[roster["id"].str[0] == "B"].copy()
    
    for r in [roster_A, roster_B]:
        
        group_nums = np.tile(np.arange(5), 5)[:len(r)]
        
        np.random.seed(123)
        np.random.shuffle(group_nums)
        r["group"] = group_nums
        r = r.sort_values(by = "group")
        r["presented"] = False
        section = r["id"].str[0].iloc[0]
        
        for i in range(num_groups):
            
            p = f"utils/teams/{section}"
            path = Path(p)
            path.mkdir(parents = True, exist_ok = True)
            
            sub = r[r["group"] == i].to_csv(p + f"/{i}.csv", index = False)

def shuffle(section = "A"):
    console = Console()
    panels = []
    path = f"utils/teams/{section}"
    for team in os.listdir(path):
        
        df = pd.read_csv(f"{path}/{team}")
        
        if np.all(df["presented"]):
            df["presented"] = False
                        
        df["r"] = np.random.rand(len(df))
        df = df.sort_values(by = ["presented", "r"])
        
        # presented is the 3rd column
        df.iloc[0, 3] = True
        
        df[["Student", "id", "group", "presented"]].to_csv(f"{path}/{team}", index = False)
        
        panel_str = ""

        for i in range(len(df)):
            
            if i == 0:    
                print('\033[1m' + "\033[94m")
                
            name = df["Student"].iloc[i]
            panel_str += format_student(name, i) + "\n"
            
        panels.append(Panel(panel_str))

    console.print(Columns(panels))
    
if __name__ == "__main__":       
    if sys.argv[1] == "assign":
        assign_ids()
    elif sys.argv[1] == "teams":
        form_teams(5)
    else: 
        shuffle(section = sys.argv[2])
