import os
import json
import git
from datetime import datetime, timedelta

DATASETS_DIR = os.path.join(os.path.dirname(__file__), 'datasets')
REPOSITORIES = [
    "https://github.com/shramos/Awesome-Cybersecurity-Datasets.git",
    "https://github.com/ensarseker1/Datasets-for-Cybersecurity.git",
    "https://github.com/mmacas11/Cybersecurity-Datasets.git",
    "https://github.com/PEASEC/cybersecurity_dataset.git"
]

LAST_UPDATE_FILE = os.path.join(DATASETS_DIR, 'last_update.txt')

def initialize_datasets():
    """Initialize dataset repositories and update mechanism"""
    os.makedirs(DATASETS_DIR, exist_ok=True)
    
    for repo_url in REPOSITORIES:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = os.path.join(DATASETS_DIR, repo_name)
        
        if not os.path.exists(repo_path):
            print(f"Cloning {repo_name}...")
            git.Repo.clone_from(repo_url, repo_path)
        else:
            print(f"Repository {repo_name} already exists, skipping clone.")

def check_and_update_datasets():
    """Check and update datasets if older than 7 days"""
    if not os.path.exists(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE, 'w') as f:
            f.write(datetime.now().isoformat())
        return
    
    with open(LAST_UPDATE_FILE, 'r') as f:
        last_update = datetime.fromisoformat(f.read())
    
    if datetime.now() - last_update > timedelta(days=7):
        print("Updating datasets...")
        for repo_name in os.listdir(DATASETS_DIR):
            repo_path = os.path.join(DATASETS_DIR, repo_name)
            if os.path.isdir(repo_path):
                try:
                    repo = git.Repo(repo_path)
                    repo.remotes.origin.pull()
                    print(f"Updated {repo_name}")
                except Exception as e:
                    print(f"Error updating {repo_name}: {str(e)}")
        
        with open(LAST_UPDATE_FILE, 'w') as f:
            f.write(datetime.now().isoformat())

def load_dataset_content():
    """Load and combine JSON datasets"""
    combined_data = []
    for repo_name in os.listdir(DATASETS_DIR):
        repo_path = os.path.join(DATASETS_DIR, repo_name)
        if os.path.isdir(repo_path):
            for root, _, files in os.walk(repo_path):
                for file in files:
                    if file.endswith('.json'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                                combined_data.append(data)
                        except Exception as e:
                            print(f"Error loading {file_path}: {str(e)}")
    return combined_data
