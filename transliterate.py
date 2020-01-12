#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import json 
import MeCab

from typing import List, Dict, Tuple

wakati = MeCab.Tagger("-Owakati")
yomi = MeCab.Tagger("-Oyomi")

def transliterate(text: str) -> Tuple[List[str], List[str]]:
    words = wakati.parse(text).split()
    kana : List[str] = []

    for word in words:
        kana.append(yomi.parse(word).strip())
    
    return words, kana

def load_data() -> List[Dict]:
    with open(os.path.join("resources", "data.json"), "r", encoding="utf-8") as in_file:
        return json.load(in_file)

def save_data(entries: List[Dict]):
    with open(os.path.join("resources", "data.json"), "w", encoding="utf-8") as out_file:
        return json.dump(entries, out_file, indent=4, ensure_ascii=False, sort_keys=True)

def main():
    entries = load_data()

    for entry in entries:
        # Transliteratte the main entry.
        words, kana = transliterate(entry["data"]["entry_name"])
        entry["data"]["kana"] = "".join(kana)

        # Transliterate the examples.
        for example in entry["examples"]:
            words, kana = transliterate(example["jp"])
            example["jp_words"] = words
            example["jp_words_kana"] = kana
    
    save_data(entries)

if __name__ == "__main__":
    main()


