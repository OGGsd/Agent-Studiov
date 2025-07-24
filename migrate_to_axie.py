import os
import shutil
import re
from pathlib import Path

def replace_in_file(file_path, old_text, new_text):
    """Replace text in a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_content = content.replace(old_text, new_text)
    new_content = re.sub(r'from langflow\.', 'from axie_studio.', new_content)
    new_content = re.sub(r'import langflow\.', 'import axie_studio.', new_content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def rename_directory():
    """Rename the main backend directory."""
    old_path = "src/backend/base/langflow"
    new_path = "src/backend/base/axie_studio"
    
    if os.path.exists(old_path):
        # Create new directory if it doesn't exist
        os.makedirs(new_path, exist_ok=True)
        
        # Copy contents
        for item in os.listdir(old_path):
            s = os.path.join(old_path, item)
            d = os.path.join(new_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        
        # Remove old directory
        shutil.rmtree(old_path)

def update_imports_and_references():
    """Update imports and references in all Python files."""
    backend_dir = "src/backend"
    
    for root, _, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                replace_in_file(file_path, 'langflow', 'axie_studio')

def update_environment_variables():
    """Update environment variable names in configuration files."""
    files_to_update = [
        'src/backend/base/axie_studio/settings.py',
        'src/backend/base/axie_studio/main.py',
        'src/backend/base/axie_studio/server.py',
        'pyproject.toml',
        'README.md'
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            replace_in_file(file_path, 'LANGFLOW_', 'AXIE_STUDIO_')

def update_database_references():
    """Update database file names and references."""
    old_db = "src/backend/base/axie_studio/langflow.db"
    new_db = "src/backend/base/axie_studio/axie_studio.db"
    
    if os.path.exists(old_db):
        shutil.move(old_db, new_db)
    
    # Update related files
    for ext in ['-shm', '-wal']:
        old_file = old_db + ext
        new_file = new_db + ext
        if os.path.exists(old_file):
            shutil.move(old_file, new_file)

def update_alembic():
    """Update Alembic migration files."""
    alembic_dir = "src/backend/base/axie_studio/alembic"
    
    if os.path.exists(alembic_dir):
        for root, _, files in os.walk(alembic_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    replace_in_file(file_path, 'langflow', 'axie_studio')

def main():
    """Main migration function."""
    print("Starting migration to Axie Studio...")
    
    # Create backup
    backup_dir = "backup_langflow"
    print(f"Creating backup in {backup_dir}...")
    shutil.copytree("src/backend/base/langflow", backup_dir, dirs_exist_ok=True)
    
    try:
        # Perform migration steps
        print("Renaming main directory...")
        rename_directory()
        
        print("Updating imports and references...")
        update_imports_and_references()
        
        print("Updating environment variables...")
        update_environment_variables()
        
        print("Updating database references...")
        update_database_references()
        
        print("Updating Alembic configuration...")
        update_alembic()
        
        print("Migration completed successfully!")
        print("Please review the changes and test thoroughly before committing.")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        print("Restoring from backup...")
        shutil.rmtree("src/backend/base/axie_studio", ignore_errors=True)
        shutil.copytree(backup_dir, "src/backend/base/langflow")
        print("Backup restored.")
        raise

if __name__ == "__main__":
    main() 