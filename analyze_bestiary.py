import pandas as pd

try:
    df = pd.read_excel('final_bestiary.xlsx')
    
    print("=== DECENNIUM'S DESCENT BESTIARY ANALYSIS ===")
    print(f"Total creatures: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    
    print("\n=== SAMPLE CREATURES ===")
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        print(f"{i+1}. {row['Name']} ({row['Size']} {row['Type']}, CR {row['Challenge']})")
    
    print("\n=== CREATURE TYPES ===")
    type_counts = df['Type'].value_counts()
    for creature_type, count in type_counts.head(10).items():
        print(f"{creature_type}: {count}")
    
    print("\n=== CHALLENGE RATINGS ===")
    cr_counts = df['Challenge'].value_counts().sort_index()
    for cr, count in cr_counts.head(15).items():
        print(f"CR {cr}: {count} creatures")
    
    print("\n=== SIZE DISTRIBUTION ===")
    size_counts = df['Size'].value_counts()
    for size, count in size_counts.items():
        print(f"{size}: {count}")
    
    print("\n=== NOTABLE FEATURES ===")
    print(f"- Unique creature names: {df['Name'].nunique()}")
    print(f"- Different creature types: {df['Type'].nunique()}")
    print(f"- Challenge rating range: {df['Challenge'].min()} to {df['Challenge'].max()}")
    
    # Check for loot system
    loot_cols = [col for col in df.columns if 'loot' in col.lower() or 'tier' in col.lower()]
    if loot_cols:
        print(f"\n=== LOOT SYSTEM ===")
        print(f"Loot-related columns: {len(loot_cols)}")
        for col in loot_cols[:5]:  # Show first 5 loot columns
            print(f"- {col}")
    
except Exception as e:
    print(f"Error: {e}")