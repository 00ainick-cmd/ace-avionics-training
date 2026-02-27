import pandas as pd
excel_path = r"C:\Users\nickb\Downloads\CAET Prep Course Question Bank\CAET_Node_Build_Master_Sheet_v1.xlsx"
df = pd.read_excel(excel_path, sheet_name=None)
for sheet_name, sheet_df in df.items():
    print(f"Sheet: {sheet_name}")
    print("Columns:", sheet_df.columns.tolist())
    print(sheet_df.head(2).to_dict(orient='records'))
    print("-" * 50)
