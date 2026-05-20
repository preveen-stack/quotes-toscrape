#!/usr/bin/env python3

import json
import random
import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://quotes.toscrape.com"
STATE_FILE = Path.home() / ".quotes_seen.json"

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

quotes = []

for quote in soup.select(".quote"):
    text = quote.select_one(".text").get_text(strip=True)
    author = quote.select_one(".author").get_text(strip=True)
    quotes.append(f"{text} — {author}")

# Load previously seen quotes
if STATE_FILE.exists():
    seen = set(json.loads(STATE_FILE.read_text()))
else:
    seen = set()

remaining = [q for q in quotes if q not in seen]

# Reset when all quotes used
if not remaining:
    seen = set()
    remaining = quotes

selected = random.choice(remaining)

print("\n" + selected + "\n")

seen.add(selected)
STATE_FILE.write_text(json.dumps(list(seen)))
