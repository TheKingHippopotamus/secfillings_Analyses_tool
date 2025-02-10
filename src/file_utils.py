import os
import re

def ensure_directory_exists(directory):
    os.makedirs(directory, exist_ok=True)

def clean_filename(name):
    return re.sub(r'[^A-Za-z0-9_-]', '_', name).strip('_')
