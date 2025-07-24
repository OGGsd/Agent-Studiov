#!/usr/bin/env python3
import os
import re

def fix_imports_in_file(file_path):
    """Fix langflow imports to axie_studio in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace imports
        original_content = content
        content = re.sub(r'from langflow\.', 'from axie_studio.', content)
        content = re.sub(r'import langflow\.', 'import axie_studio.', content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_imports_in_directory(directory):
    """Fix imports in all Python files in a directory recursively."""
    fixed_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if fix_imports_in_file(file_path):
                    fixed_count += 1
    return fixed_count

if __name__ == "__main__":
    axie_studio_dir = "src/backend/base/axie_studio"
    if os.path.exists(axie_studio_dir):
        print(f"Fixing imports in {axie_studio_dir}...")
        count = fix_imports_in_directory(axie_studio_dir)
        print(f"Fixed imports in {count} files.")
    else:
        print(f"Directory {axie_studio_dir} not found!")

    # Also fix imports in the serialization directory
    serialization_dir = "src/backend/base/axie_studio/serialization"
    if os.path.exists(serialization_dir):
        print(f"Fixing imports in {serialization_dir}...")
        count = fix_imports_in_directory(serialization_dir)
        print(f"Fixed imports in {count} files in serialization.")
    else:
        print(f"Directory {serialization_dir} not found!")
