import pandas as pd
import os

def read_excel_file(file_path):
    """Read and display Excel file contents"""
    try:
        print(f"\n{'='*80}")
        print(f"Reading Excel file: {os.path.basename(file_path)}")
        print(f"{'='*80}")
        
        # Read the Excel file
        excel_file = pd.ExcelFile(file_path)
        
        print(f"\nSheet names: {excel_file.sheet_names}")
        print(f"Number of sheets: {len(excel_file.sheet_names)}")
        
        # Read each sheet
        for sheet_name in excel_file.sheet_names:
            print(f"\n{'-'*60}")
            print(f"Sheet: {sheet_name}")
            print(f"{'-'*60}")
            
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"Shape: {df.shape} (rows, columns)")
            print(f"Columns: {list(df.columns)}")
            
            # Display first few rows
            print("\nFirst 10 rows:")
            print(df.head(10).to_string(index=False))
            
            # Show data types
            print("\nData types:")
            print(df.dtypes.to_string())
            
            # Show basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                print("\nNumeric column statistics:")
                print(df[numeric_cols].describe().to_string())
            
            # Show unique values for categorical columns (if not too many)
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                unique_vals = df[col].unique()
                if len(unique_vals) <= 20:  # Only show if reasonable number
                    print(f"\nUnique values in '{col}': {list(unique_vals)}")
                else:
                    print(f"\nColumn '{col}' has {len(unique_vals)} unique values")
        
        return True
        
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return False

def main():
    excel_file = r'C:\Users\cbord\OneDrive\Documents\GitHub\Arena Fighter\final_bestiary.xlsx'
    
    if os.path.exists(excel_file):
        success = read_excel_file(excel_file)
        if success:
            print(f"\n{'='*80}")
            print("Excel file read successfully!")
            print(f"{'='*80}")
    else:
        print(f"Excel file not found: {excel_file}")

if __name__ == "__main__":
    main()