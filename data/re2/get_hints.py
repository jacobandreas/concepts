#!/usr/bin/env python2

from collections import defaultdict
import csv
import json
from nltk.tokenize import word_tokenize
import os
import re

templates = defaultdict(list)
hints = {}

exclude = ["'", '"', "`", ".", "\\"]

with open("data.json") as data_f:
    data = json.load(data_f)["train"]

for name in os.listdir("turk"):
    path = os.path.join("turk", name)
    with open(path) as turk_f:
        reader = csv.DictReader(turk_f)
        for row in reader:
            datum_id = int(row["Input.id"])
            hint = row["Answer.hint_text"]
            words = word_tokenize(hint)
            hint = " ".join(words)
            hint = hint.lower()
            for e in exclude:
                hint = hint.replace(e, "")
            hint = hint.replace("-", " - ")
            hint = hint.replace("+", " + ")
            hint = hint.replace("/", " / ")
            hint = re.sub(r"\s+", " ", hint)

            datum = data[datum_id]
            special_b = datum["before"].split(")(")[1]
            special_b = special_b.replace(".", "").replace("[^aeiou]", "").replace("[aeiou]", "")
            special_a = datum["after"][2:-2]
            special_a = special_a.replace("\\2", "")

            a_exploded = " ".join(special_a)
            b_exploded = " ".join(special_b)

            pattern_before = datum["before"].replace("[aeiou]", "V").replace("[^aeiou]", "C")
            pattern_before = re.sub("[a-z]", "l", pattern_before)
            pattern_after = datum["after"][2:-2]
            pattern_after = re.sub("[a-z]+", "l", pattern_after)

            template = hint

            if special_a:
                template = re.sub(r"\b%s\b" % special_a, "AFTER", hint)
                hint = re.sub(r"\b%s\b" % special_a, a_exploded, hint)
            if special_b:
                template = re.sub(r"\b%s\b" % special_b, "BEFORE", hint)
                hint = re.sub(r"\b%s\b" % special_b, b_exploded, hint)

            templates[pattern_before + "@" + pattern_after].append(template)

            #print (pattern_before, pattern_after), hint
            assert datum_id not in hints
            hints[datum_id] = hint

with open("hints.json", "w") as hint_f:
    json.dump(hints, hint_f)

print len(hints)

with open("templates.json", "w") as template_f:
    json.dump(templates, template_f)