#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from typing import List, Dict

from utils import save_data

JAPANESE_CHARACTERS = r'\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf'
ANTI_JAPANESE_CHARACTERS = r'^\u3000-\u303f^\u3040-\u309f^\u30a0-\u30ff^\uff00-\uff9f^\u4e00-\u9faf^\u3400-\u4dbf'

EXCEPTIONS = [
        "1864	0 rei n. zero",
        "1868	CM shiiemu n. commercial",
        "2613	NHK enueichikei, enuechikei n. Nihon",
        "2710	IT aitii n. IT",
        "2763	PC piishii n. personal computer",
        "3396	OS ooesu n. operating system",
        "3502	Eメール ii meeru n. e-mail",
        "3703	DVD diibuidii n. DVD",
        "3900	HP hoomupeeji n. home page",
        "3911	Tシャツ tii shatsu n. T-shirt",
        "4137	TV terebi n. television",
        "4175	ID aidii n. identification, ID",
        "4343	WWW daburyuudaburyuudaburyuu n. World Wide Web",
        "4584	DNA diienuee n. DNA, deoxyribonucleic acid",
        "4787	OB oobii n. OB (old boy), alumnus",
        "4916	URL yuuaarueru n. URL, Uniform Resource Locator"
    ]

PARTS_OF_SPEECH = [
    "p. case",
    "p.",
    "aux.",
    "p. conj.",
    "cp.",
    "n.",
    "interj.",
    "v.",
    "p. disc.",
    "adn.",
    "conj.",
    "adv.",
    "pron.",
    "i-adj.",
    "na-adj.",
    "num"
]

ENTRY_START_PATTERN = re.compile(r'^\d+\s(\(\u304A\)s?)?[' + JAPANESE_CHARACTERS + ']+')
ENTRY_END_LINE_PATTERN = re.compile(r'\d+\s\|\s\d\.\d\d(?:\s\|\s\w+)?$')
ENTRY_END_LINE_ANYWHERE_PATTERN = re.compile(r'\d+\s\|\s\d\.\d\d(?:\s\|\s\w+)?')
PARTS_OF_SPEECH_PATTERN = re.compile(r'(' + r'|'.join([re.escape(x) for x in PARTS_OF_SPEECH]) + r')')
ID_JAPANESE_ROMAJI_PATTERN = re.compile(r'^(\d+)+\s([\w\s\.\,\(\)\<' + JAPANESE_CHARACTERS + r']+)\s([\w\(\)\-]+)')
EXAMPLE_PATTERN  = re.compile(r'[' + JAPANESE_CHARACTERS + r']+\s\u2014+\s[' + ANTI_JAPANESE_CHARACTERS + r']+')

def read_data() -> List[List[str]]:

    with open(os.path.join("resources", "data.txt"), 'r',encoding='utf8') as in_file:
        lines = in_file.readlines()

    
    entry_lines : List[str] = []
    entries = []

    for line in lines:
        line = line.strip()
        if ENTRY_START_PATTERN.match(line):
            entry_lines = []
        else:
            if line in EXCEPTIONS:
                entry_lines = []

        entry_lines.append(line)
        if ENTRY_END_LINE_PATTERN.search(line):
            entries.append(entry_lines)

    return entries

def parse_entries(entries: List[List[str]]) -> List[Dict]:
    parsed_entries = []
    for entry in entries:
        parsed_entry = parse_entry(entry)
        parsed_entries.append(parsed_entry)
    return parsed_entries

def parse_entry(entry: List[str]) -> Dict:
    data = parse_header(entry[0])
    examples = parse_example(entry[1:])
    return {"data": data, "examples": examples}

def parse_header(header: str) -> Dict:
    splits = PARTS_OF_SPEECH_PATTERN.split(header)
    
    id_jp_roj = ID_JAPANESE_ROMAJI_PATTERN.match(splits[0])
    assert id_jp_roj is not None
    id, japanese, romanji = id_jp_roj.groups()

    usages = splits[1:]
    assert len(usages) % 2 == 0
    usages_dict = {usages[i]: usages[i+1] for i in range(0, len(usages)//2, 2)}

    return {
        "entry_id": id,
        "entry_name": japanese,
        "romaji": romanji,
        "usages": usages_dict
    }

def parse_example(example_lines : List[str]) -> List[Dict[str, str]]:
    example_text = " ".join(example_lines)
    example_text = ENTRY_END_LINE_PATTERN.sub("", example_text)
    example_text = example_text.strip()

    examples = EXAMPLE_PATTERN.findall(example_text)

    parsed_examples : List[Dict[str, str]] = []
    for example in examples:
        japanese, english = example.split(u'\u2014')
        english = ENTRY_END_LINE_ANYWHERE_PATTERN.split(english)[0]
        # Changes all whitespace to spaces and strips
        english = " ".join(english.split())
        
        parsed_examples.append({
            "jp": japanese.strip(),
            "en": english
        })
    return parsed_examples

def main():
    raw_entries = read_data()
    parsed_entries = parse_entries(raw_entries)
    save_data(parsed_entries)

if __name__ == "__main__":
    main()
