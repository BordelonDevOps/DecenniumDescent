import pandas as pd
import os

def examine_excel_files():
    """Examine all Excel files in the directory"""
    excel_files = ['final_bestiary.xlsx', 'decennium_descent_crafting_recipes_validated.xlsx']
    
    for file_path in excel_files:
        if os.path.exists(file_path):
            print(f"\n{'='*80}")
            print(f"Examining: {file_path}")
            print(f"{'='*80}")
            
            try:
                xl = pd.ExcelFile(file_path)
                print(f"Sheets: {xl.sheet_names}")
                
                for sheet in xl.sheet_names:
                    df = pd.read_excel(file_path, sheet_name=sheet)
                    print(f"\n--- Sheet: {sheet} ---")
                    print(f"Shape: {df.shape} (rows, columns)")
                    print(f"Columns: {list(df.columns)}")
                    
                    if len(df) > 0:
                        print("\nFirst 3 rows:")
                        print(df.head(3).to_string(index=False))
                    else:
                        print("No data in this sheet")
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    examine_excel_files()