#!/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

with open(os.path.join("resources", "data.txt"), 'r',encoding='utf8') as in_file:
    lines = in_file.readlines()

JAPANESE_CHARACTERS = r'[\u3000-\u303f\u3040-\u309f\u30a0-\u30ff\uff00-\uff9f\u4e00-\u9faf\u3400-\u4dbf]+'

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

entry_start_pattern = re.compile(r'^\d+\s(\(\u304A\)s?)?'+JAPANESE_CHARACTERS)
entry_end_line_pattern = re.compile(r'\d+\s\|\s\d\.\d\d')
entry_lines = []
entries = []

for line in lines:
    line = line.strip()
    if entry_start_pattern.match(line):
        entry_lines = []
    else:
        if line in EXCEPTIONS:
            entry_lines = []

    entry_lines.append(line)
    if entry_end_line_pattern.search(line):
        entries.append(entry_lines)

print("Length: ", len(entries))