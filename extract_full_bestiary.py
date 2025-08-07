import pandas as pd
import json
import numpy as np

def extract_full_bestiary():
    try:
        # Load the Excel file
        df = pd.read_excel('final_bestiary.xlsx')
        
        print(f"Loaded {len(df)} creatures from bestiary")
        print(f"Columns: {list(df.columns)}")
        
        # Filter out "Ul'nath, the Hollow Dream" - keep it hidden
        df_filtered = df[df['Name'] != "Ul'nath, the Hollow Dream"]
        print(f"After filtering hidden creatures: {len(df_filtered)} creatures")
        
        # Convert to list of dictionaries
        creatures = []
        
        for _, row in df_filtered.iterrows():
            # Use the actual column names from the Excel file
            creature = {
                'name': str(row.get('Name', 'Unknown')),
                'type': str(row.get('Type', 'Unknown')),
                'size': str(row.get('Size', 'Medium')),
                'challengeRating': str(row.get('Challenge', '0')),
                'xp': int(row.get('XP', 0)) if pd.notna(row.get('XP')) else 0,
                'alignment': str(row.get('Alignment', '')),
                'tags': str(row.get('Tags', '')),
                'zoneFound': str(row.get('Zone Found', '')),
                # Since AC, HP, Speed, and ability scores aren't in the Excel, we'll calculate them
                'armorClass': 10,  # Will be calculated based on CR
                'hitPoints': 1,    # Will be calculated based on CR
                'speed': '30 ft.', # Default speed
                'abilities': {
                    'strength': 10,
                    'dexterity': 10,
                    'constitution': 10,
                    'intelligence': 10,
                    'wisdom': 10,
                    'charisma': 10
                },
                'skills': '',
                'senses': '',
                'languages': '',
                'description': f"A {row.get('Size', 'Medium').lower()} {row.get('Type', 'creature').lower()} found in {row.get('Zone Found', 'various locations')}.",
                'loot': {
                    'tier1': {
                        'drop': str(row.get('Tier 1 Drop', '')),
                        'rate': str(row.get('Tier 1 Rate', '')),
                        'value': str(row.get('Tier 1 Value', ''))
                    },
                    'tier2': {
                        'drop': str(row.get('Tier 2 Drop', '')),
                        'rate': str(row.get('Tier 2 Rate', '')),
                        'value': str(row.get('Tier 2 Value', ''))
                    },
                    'tier3': {
                        'drop': str(row.get('Tier 3 Drop', '')),
                        'rate': str(row.get('Tier 3 Rate', '')),
                        'value': str(row.get('Tier 3 Value', ''))
                    }
                }
            }
            creatures.append(creature)
        
        # Save to JSON file
        with open('src/bestiary_data_full.json', 'w', encoding='utf-8') as f:
            json.dump(creatures, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully extracted {len(creatures)} creatures to bestiary_data_full.json")
        
        # Print some statistics
        types = [c['type'] for c in creatures]
        type_counts = {}
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1
        
        print("\nCreature type distribution:")
        for creature_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {creature_type}: {count}")
        
        # Print CR distribution
        crs = [c['challengeRating'] for c in creatures]
        cr_counts = {}
        for cr in crs:
            cr_counts[cr] = cr_counts.get(cr, 0) + 1
        
        print("\nChallenge Rating distribution:")
        for cr, count in sorted(cr_counts.items(), key=lambda x: float(x[0]) if x[0].replace('.', '').isdigit() else 0):
            print(f"  CR {cr}: {count}")
        
        # Print some sample creatures
        print("\nSample creatures:")
        for i, creature in enumerate(creatures[:5]):
            print(f"  {creature['name']} - {creature['type']} - CR {creature['challengeRating']} - {creature['zoneFound']}")
        
        return creatures
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    extract_full_bestiary()