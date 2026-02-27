import pandas as pd
import json
import os

excel_path = r"C:\Users\nickb\Downloads\CAET Prep Course Question Bank\CAET_Node_Build_Master_Sheet_v1.xlsx"
output_path = r"C:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\course_index.json"

df = pd.read_excel(excel_path, sheet_name="Nodes_Master")

course_index = {}

for _, row in df.iterrows():
    if pd.isna(row.get("Objective Keys")):
        continue
        
    objective_keys = str(row["Objective Keys"]).split(",")
    node_id = row.get("Node ID", "")
    node_title = row.get("Node Title", "")
    
    # Map the general category to a mock rise module for now
    # We can refine these placeholders later based on exact module names
    world = str(row.get("World", ""))
    mock_rise_url = ""
    if world == "W1":
        mock_rise_url = "training/caet/mod8-shop-safety/index.html"
    elif world == "W2":
        mock_rise_url = "training/caet/mod1-maintenance-regs/index.html"
        
    for key in objective_keys:
        key = key.strip()
        if not key: continue
        
        course_index[key] = {
            "node_id": node_id,
            "node_title": node_title,
            "journey_url": f"journey.html?node={node_id}",
            "rise_url": mock_rise_url,      # To be updated by user
            "notebook_url": "",             # To be updated by user
            "textbook_url": ""              # To be updated by user
        }

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(course_index, f, indent=2)

print(f"Successfully exported {len(course_index)} LO mappings to {output_path}")
