#!/usr/bin/env python3
"""
Quick script to fix all langflow documentation URLs in starter project templates.
"""

import json
import os
import re
from pathlib import Path

def fix_langflow_docs_in_json(file_path):
    """Fix langflow documentation URLs in a JSON file by properly parsing and modifying JSON."""
    try:
        # Load the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Track if any changes were made
        changes_made = False

        # Function to recursively process the JSON structure
        def process_value(obj):
            nonlocal changes_made
            if isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = process_value(value)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    obj[i] = process_value(item)
            elif isinstance(obj, str):
                original = obj
                # Replace langflow documentation URLs
                obj = re.sub(r'https://docs\.langflow\.org[^\s"]*', 'https://docs.axiestudio.com', obj)
                # Replace langflow references
                obj = re.sub(r'\bLangflow\b', 'Axie Studio', obj)
                # Replace langflow.org references
                obj = re.sub(r'langflow\.org', 'axiestudio.com', obj)
                if obj != original:
                    changes_made = True
            return obj

        # Process the entire JSON structure
        data = process_value(data)

        # If changes were made, write back to file
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all starter project templates."""
    print("🔧 Fixing langflow documentation URLs in starter project templates...")
    
    # Path to starter projects
    script_dir = Path(__file__).parent
    starter_projects_dir = script_dir / "src/backend/base/axie_studio/initial_setup/starter_projects"
    
    if not starter_projects_dir.exists():
        print(f"❌ Directory not found: {starter_projects_dir}")
        return
    
    fixed_count = 0
    total_count = 0
    
    # Process all JSON files
    for json_file in starter_projects_dir.glob("*.json"):
        total_count += 1
        if fix_langflow_docs_in_json(json_file):
            print(f"✅ Fixed: {json_file.name}")
            fixed_count += 1
        else:
            print(f"ℹ️ No changes needed: {json_file.name}")
    
    print(f"\n🎉 Processed {total_count} files, fixed {fixed_count} files!")

if __name__ == "__main__":
    main()
