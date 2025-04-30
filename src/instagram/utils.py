# instagram/utils.py
import csv

def load_credentials_from_csv(file_path):
    """Load Instagram credentials from CSV."""
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                return row['username'], row['password']
    except Exception as e:
        print(f"❌ Failed to load credentials: {e}")
        return None, None