# storage.py (helper functions to read/write game records)
import os
import json

# Save a dictionary as a line in a JSON Lines file
def save_jsonl(filepath, data):
    with open(filepath, "a", encoding="utf-8") as f:
        json.dump(data, f)
        f.write("\n")

# Read all entries from a JSON Lines file
def read_jsonl(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
