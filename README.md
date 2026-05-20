# Quote Scraper CLI

A simple Python command-line program that fetches quotes from
[Quotes to Scrape](https://quotes.toscrape.com?utm_source=chatgpt.com)
and displays a random quote each time you run it.

---

## Features

* Fetches quotes from a website
* Displays a random quote on every run
* Optional version that avoids repeats until all quotes are shown
* Lightweight and easy to modify
* Works on Linux, macOS, and Windows

---

## Requirements

* Python 3.7+
* Internet connection

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

# Basic Version

## File: `quotes.py`

```python
#!/usr/bin/env python3

import random
import requests
from bs4 import BeautifulSoup

URL = "https://quotes.toscrape.com"

# Fetch quotes from the website
response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

quotes = []

for quote in soup.select(".quote"):
    text = quote.select_one(".text").get_text(strip=True)
    author = quote.select_one(".author").get_text(strip=True)
    quotes.append((text, author))

# Pick a random quote each run
quote, author = random.choice(quotes)

print(f"\n{quote}\n    — {author}\n")
```

---

## Run

```bash
python3 quotes.py
```

Example output:

```text
“The world as we have created it is a process of our thinking.”
    — Albert Einstein
```

---

# Non-Repeating Version

This version remembers previously shown quotes and avoids repeats until all quotes have been displayed.

## File: `quotes_no_repeat.py`

```python
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
```

---

## Run

```bash
python3 quotes_no_repeat.py
```

---

# Make Executable (Linux/macOS)

```bash
chmod +x quotes.py
./quotes.py
```

---

# Possible Improvements

* Fetch quotes from all pages
* Add quote categories/tags
* Offline caching
* Terminal colors
* Daily quote mode
* Export favorite quotes

---

# License

MIT License

