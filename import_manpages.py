import os
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["explainshell"]
collection = db["manpage"]

MANPAGE_ROOT = "manpages"
count = 0
errors = 0

# Walk through subdirectories (e.g., manpages/1/, manpages/8/, etc.)
for dirpath, _, filenames in os.walk(MANPAGE_ROOT):
    for filename in filenames:
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(dirpath, filename)
        try:
            with open(filepath, "r") as f:
                doc = json.load(f)
                collection.insert_one(doc)
                count += 1
        except Exception as e:
            print(f"❌ Failed to import {filepath}: {e}")
            errors += 1

print(f"\n✅ Imported {count} manpages with {errors} errors.")
