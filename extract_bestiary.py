import pandas as pd
import json
import sys

def extract_bestiary_data():
    try:
        # Read the Excel file
        df = pd.read_excel('final_bestiary.xlsx')
        
        print(f"Loaded {len(df)} creatures from bestiary")
        print(f"Columns: {list(df.columns)}")
        
        # Extract first 50 creatures for initial integration (excluding Ul'nath)
        creatures = []
        
        for index, row in df.head(50).iterrows():
            # Skip Ul'nath, the Hollow Dream
            if 'Ul\'nath' in str(row.get('Name', '')) or 'Hollow Dream' in str(row.get('Name', '')):
                print(f"Skipping {row.get('Name', 'Unknown')} - keeping it hidden")
                continue
                
            creature = {
                'name': str(row.get('Name', 'Unknown')),
                'type': str(row.get('Type', 'Unknown')),
                'size': str(row.get('Size', 'Medium')),
                'challengeRating': str(row.get('Challenge Rating', '0')),
                'armorClass': int(row.get('Armor Class', 10)) if pd.notna(row.get('Armor Class')) else 10,
                'hitPoints': int(row.get('Hit Points', 1)) if pd.notna(row.get('Hit Points')) else 1,
                'speed': str(row.get('Speed', '30 ft.')),
                'abilities': {
                    'strength': int(row.get('STR', 10)) if pd.notna(row.get('STR')) else 10,
                    'dexterity': int(row.get('DEX', 10)) if pd.notna(row.get('DEX')) else 10,
                    'constitution': int(row.get('CON', 10)) if pd.notna(row.get('CON')) else 10,
                    'intelligence': int(row.get('INT', 10)) if pd.notna(row.get('INT')) else 10,
                    'wisdom': int(row.get('WIS', 10)) if pd.notna(row.get('WIS')) else 10,
                    'charisma': int(row.get('CHA', 10)) if pd.notna(row.get('CHA')) else 10
                },
                'skills': str(row.get('Skills', 'None')),
                'senses': str(row.get('Senses', 'Passive Perception 10')),
                'languages': str(row.get('Languages', 'None')),
                'description': str(row.get('Description', 'A mysterious creature.')),
                # Loot information
                'loot': {
                    'tier1': {
                        'drop': str(row.get('Tier 1 Drop', 'None')),
                        'rate': str(row.get('Tier 1 Rate', '0%')),
                        'value': str(row.get('Tier 1 Value', '0 gp'))
                    },
                    'tier2': {
                        'drop': str(row.get('Tier 2 Drop', 'None')),
                        'rate': str(row.get('Tier 2 Rate', '0%')),
                        'value': str(row.get('Tier 2 Value', '0 gp'))
                    }
                }
            }
            
            creatures.append(creature)
            
        print(f"Extracted {len(creatures)} creatures (excluding hidden ones)")
        
        # Save to JSON file
        with open('bestiary_data.json', 'w', encoding='utf-8') as f:
            json.dump(creatures, f, indent=2, ensure_ascii=False)
            
        print("Bestiary data saved to bestiary_data.json")
        
        # Print sample creature for verification
        if creatures:
            print("\n=== SAMPLE CREATURE ===")
            print(json.dumps(creatures[0], indent=2))
            
        return creatures
        
    except Exception as e:
        print(f"Error extracting bestiary data: {e}")
        return []

if __name__ == "__main__":
    extract_bestiary_data()