from pathlib import Path

def safe_filename(string):
    keepcharacters = (' ','.','_')
    return "".join(c for c in string if c.isalnum() or c in keepcharacters).rstrip()

def create_path(the_path):
    Path(the_path).mkdir(parents=True, exist_ok=True)
