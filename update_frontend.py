import os
import re
from pathlib import Path

def update_file(file_path):
    """Update content in frontend files."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Update environment variables
    replacements = {
        'LANGFLOW_': 'AXIE_STUDIO_',
        'langflow-ai': 'OGGsd',
        'Langflow Chat': 'Axie Studio Chat',
        'ENABLE_LANGFLOW_STORE': 'ENABLE_AXIE_STUDIO_STORE',
        'access_token_langflow': 'access_token_axie',
        'apikey_tkn_langflow': 'apikey_tkn_axie',
        'auto_login_langflow': 'auto_login_axie',
        'refresh_token_langflow': 'refresh_token_axie',
        'github.com/langflow-ai/': 'github.com/OGGsd/',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(directory):
    """Process all frontend files in a directory recursively."""
    extensions = ('.ts', '.tsx', '.js', '.jsx', '.env')
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                update_file(file_path)

def main():
    """Main function to update frontend files."""
    print("Starting frontend update...")
    
    # Update frontend files
    frontend_dir = "src/frontend"
    if os.path.exists(frontend_dir):
        process_directory(frontend_dir)
    
    print("Frontend update completed!")

if __name__ == "__main__":
    main() 