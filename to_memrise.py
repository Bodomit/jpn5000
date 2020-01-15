import os
import csv

import jaconv
from utils import load_data


def main():
    entries = load_data()

    base_path = os.path.join("resources", "memrise")
    os.makedirs(base_path, exist_ok=True)


    # Write Entries
    with open(os.path.join(base_path, "entries.csv"), 'w', newline='') as csvfile:
        fieldnames = ["kana", "english", "common", "part"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for entry in entries:
            entry = entry["data"]
            # If katakana word, leave as is, otherwise convert to hiragana.
            if jaconv.hira2kata(entry["kana"]) == entry["entry_name"]:
                kana = entry["kana"]
            else:
                kana = jaconv.kata2hira(entry["kana"])
            
            writer.writerow({
                "kana": kana, 
                "english": "; ".join(entry["usages"].values()).strip(),
                "common": entry["entry_name"],
                "part": "; ".join(entry["usages"].keys()),
                })
    

if __name__ == "__main__":
    main()