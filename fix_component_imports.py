#!/usr/bin/env python3
"""
Quick fix for langflow.base.prompts.api_utils import errors.
This script directly updates the database to fix the specific import issue.
"""

import sqlite3
import json
import re

def fix_component_imports():
    """Fix the specific langflow import issue in the database."""
    print("🔧 Fixing langflow.base.prompts.api_utils imports...")
    
    # Connect to the SQLite database
    db_path = "src/backend/base/axie_studio/langflow.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all flows with their data
        cursor.execute("SELECT id, name, data FROM flow WHERE data IS NOT NULL")
        flows = cursor.fetchall()
        
        updated_count = 0
        
        for flow_id, flow_name, data_json in flows:
            if data_json:
                try:
                    # Parse the JSON data
                    data = json.loads(data_json)
                    
                    # Convert back to string for regex replacement
                    data_str = json.dumps(data)
                    original_data_str = data_str
                    
                    # Fix the specific problematic imports
                    replacements = [
                        (r'langflow\.base\.prompts\.api_utils', 'axie_studio.base.prompts.api_utils'),
                        (r'langflow\.custom\.custom_component\.component', 'axie_studio.custom.custom_component.component'),
                        (r'from langflow\.', 'from axie_studio.'),
                        (r'import langflow\.', 'import axie_studio.'),
                    ]
                    
                    # Apply replacements
                    for pattern, replacement in replacements:
                        data_str = re.sub(pattern, replacement, data_str)
                    
                    # If changes were made, update the database
                    if data_str != original_data_str:
                        # Update the flow in the database
                        cursor.execute(
                            "UPDATE flow SET data = ? WHERE id = ?",
                            (data_str, flow_id)
                        )
                        updated_count += 1
                        print(f"✅ Updated flow: {flow_name} (ID: {flow_id})")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Error parsing JSON for flow {flow_name}: {e}")
                except Exception as e:
                    print(f"❌ Error updating flow {flow_name}: {e}")
        
        # Commit the changes
        if updated_count > 0:
            conn.commit()
            print(f"🎉 Successfully updated {updated_count} flows!")
        else:
            print("ℹ️ No flows needed updating.")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_component_imports()
