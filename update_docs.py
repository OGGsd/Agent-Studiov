import os
import re
from pathlib import Path

def update_markdown_file(file_path):
    """Update content in markdown files."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Update common terms
    replacements = {
        'Langflow': 'Axie Studio',
        'langflow': 'axie-studio',
        'LANGFLOW_': 'AXIE_STUDIO_',
        'docs.langflow.org': 'axiestudio.se',
        'api.langflow.org': 'api.axiestudio.se',
        'github.com/langflow-ai/langflow': 'github.com/OGGsd/agent-studio',
        'langflow-ai': 'OGGsd',
        'langflow.org': 'axiestudio.se',
        'docs.axie-studio.org': 'axiestudio.se',
        'api.axie-studio.org': 'api.axiestudio.se',
        'axie-studio.org': 'axiestudio.se'
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Update code blocks
    content = re.sub(r'```python\n.*?from langflow', '```python\nfrom axie_studio', content, flags=re.DOTALL)
    content = re.sub(r'```python\n.*?import langflow', '```python\nimport axie_studio', content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_directory(directory):
    """Process all markdown files in a directory recursively."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                update_markdown_file(file_path)

def main():
    """Main function to update documentation."""
    print("Starting documentation update...")
    
    # Update main documentation
    docs_dir = "docs/docs"
    if os.path.exists(docs_dir):
        process_directory(docs_dir)
    
    # Update root documentation files
    root_docs = [
        "README.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "docs/README.md"
    ]
    
    for doc in root_docs:
        if os.path.exists(doc):
            print(f"Processing {doc}...")
            update_markdown_file(doc)
    
    print("Documentation update completed!")

if __name__ == "__main__":
    main() 