import os
import json
from typing import List, Dict

def load_data() -> List[Dict]:
    with open(os.path.join("resources", "data.json"), "r", encoding="utf-8") as in_file:
        return json.load(in_file)

def save_data(entries: List[Dict]):
    with open(os.path.join("resources", "data.json"), "w", encoding="utf-8") as out_file:
        return json.dump(entries, out_file, indent=4, ensure_ascii=False, sort_keys=True)