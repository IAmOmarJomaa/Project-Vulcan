import os

# Define the root of your project
ROOT_DIR = os.getcwd()
OUTPUT_FILE = "PROJECT_CONTEXT.txt"

# Folders to ignore to keep the context clean
IGNORE_DIRS = {'.git', '__pycache__', 'data', 'venv', 'node_modules'}
IGNORE_FILES = {OUTPUT_FILE, '.env', 'package-lock.json'}

def harvest_context():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Prune ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            
            for file in files:
                if file in IGNORE_FILES or file.endswith(('.pyc', '.png', '.jpg', '.parquet')):
                    continue
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, ROOT_DIR)
                
                outfile.write(f"LOCATION: {relative_path}\n")
                outfile.write("-" * 40 + "\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        outfile.write(f.read())
                except Exception as e:
                    outfile.write(f"[ERROR READING FILE: {e}]")
                
                outfile.write("\n\n" + "="*80 + "\n\n")

    print(f"✅ Success! All code gathered in {OUTPUT_FILE}")

if __name__ == "__main__":
    harvest_context()