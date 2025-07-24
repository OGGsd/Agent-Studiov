#!/usr/bin/env python3
"""
Comprehensive script to fix ALL langflow references in starter project templates.
This includes documentation URLs, import statements, module references, and GitHub URLs.
"""

import json
import os
import re
from pathlib import Path

def fix_all_langflow_refs_in_json(file_path):
    """Fix ALL langflow references in a JSON file by properly parsing and modifying JSON."""
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
                
                # Replace langflow.org domain references
                obj = re.sub(r'langflow\.org', 'axiestudio.com', obj)
                
                # Replace "Langflow" brand references with "Axie Studio"
                obj = re.sub(r'\bLangflow\b', 'Axie Studio', obj)
                
                # Replace langflow imports with axie_studio imports
                obj = re.sub(r'from langflow\.', 'from axie_studio.', obj)
                obj = re.sub(r'import langflow\.', 'import axie_studio.', obj)
                
                # Replace langflow module references in strings
                obj = re.sub(r'"langflow\.', '"axie_studio.', obj)
                obj = re.sub(r"'langflow\.", "'axie_studio.", obj)
                
                # Replace GitHub URLs pointing to langflow-ai/langflow
                obj = re.sub(r'https://github\.com/langflow-ai/langflow', 'https://github.com/axiestudio/axiestudio', obj, flags=re.IGNORECASE)
                obj = re.sub(r'https://raw\.githubusercontent\.com/langflow-ai/langflow', 'https://raw.githubusercontent.com/axiestudio/axiestudio', obj, flags=re.IGNORECASE)

                # Replace any remaining langflow path references in URLs
                obj = re.sub(r'/langflow/', '/axie_studio/', obj)
                obj = re.sub(r'/base/langflow/', '/base/axie_studio/', obj)

                # Replace standalone "langflow" values
                if obj.strip() == "langflow":
                    obj = "axie_studio"

                # Replace langflow in documentation URLs
                obj = re.sub(r'docs\.datastax\.com/en/langflow/', 'docs.datastax.com/en/axiestudio/', obj)

                # Replace langflow in tracking/usage strings but preserve langchain imports
                if 'langflow' in obj and 'langchain' not in obj:
                    obj = re.sub(r'\blangflow\b', 'axie_studio', obj)

                # Replace specific remaining cases
                obj = re.sub(r'LangFlow', 'Axie Studio', obj)
                obj = re.sub(r'langflow_index', 'axie_studio_index', obj)
                obj = re.sub(r'Langflows', 'Axie Studio\'s', obj)
                
                # Replace any remaining langflow references in module paths
                obj = re.sub(r'langflow\.components\.', 'axie_studio.components.', obj)
                obj = re.sub(r'langflow\.base\.', 'axie_studio.base.', obj)
                obj = re.sub(r'langflow\.custom\.', 'axie_studio.custom.', obj)
                obj = re.sub(r'langflow\.inputs\.', 'axie_studio.inputs.', obj)
                obj = re.sub(r'langflow\.io\.', 'axie_studio.io.', obj)
                obj = re.sub(r'langflow\.schema\.', 'axie_studio.schema.', obj)
                obj = re.sub(r'langflow\.template\.', 'axie_studio.template.', obj)
                obj = re.sub(r'langflow\.helpers\.', 'axie_studio.helpers.', obj)
                obj = re.sub(r'langflow\.utils\.', 'axie_studio.utils.', obj)
                obj = re.sub(r'langflow\.field_typing\.', 'axie_studio.field_typing.', obj)
                
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
    """Main function to fix all langflow references in starter project templates."""
    print("🔧 Fixing ALL langflow references in starter project templates...")
    
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
        if fix_all_langflow_refs_in_json(json_file):
            print(f"✅ Fixed: {json_file.name}")
            fixed_count += 1
        else:
            print(f"ℹ️ No changes needed: {json_file.name}")
    
    print(f"\n🎉 Processed {total_count} files, fixed {fixed_count} files!")
    print("🚀 All langflow references have been replaced with axie_studio!")

if __name__ == "__main__":
    main()
