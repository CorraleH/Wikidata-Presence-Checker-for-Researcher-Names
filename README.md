# Wikidata Presence Checker for Researcher Names

This script is designed to verify whether a list of researcher names (e.g., from academic CVs or institutional directories) exist as items in [Wikidata](https://www.wikidata.org/).

## 🧠 Purpose

Many research projects and academic initiatives benefit from structured, linked data. This script helps identify which researchers already have a corresponding item in Wikidata — an open knowledge base — and which ones do not.

## 📂 Input

The script expects a CSV file with at least one column named `name`, containing the names to be checked.

**Example CSV:**

```
name
Ana Silva
João Pereira
Carlos Souza
```

## 📤 Output

After checking each name, a new CSV file will be generated listing only those names not found in Wikidata.

Default output file: `researchers_not_found_wikidata.csv`

## ⚙️ How it works

- For each name, the script queries the Wikidata API using `wbsearchentities`.
- It applies exponential backoff in case of rate limiting (HTTP 429 errors).
- It prints progress every 10 names and saves the final results to a CSV file.

## 🛠️ Requirements

- Python 3
- pandas
- requests

Install the required packages with:

```
pip install pandas requests
```

## ⚠️ Customizing Language and User-Agent

1. Set your preferred language:
The script uses the language variable when querying the Wikidata API. Change this value to your preferred language code (e.g., 'en' for English, 'pt' for Portuguese, 'es' for Spanish).

2. Update the User-Agent header:
Wikimedia APIs require a descriptive User-Agent header for all requests. You must replace the default value in the script with your own script name, version, project URL, or contact email.
Example format: 'User-Agent': 'MyScript/1.0 (https://example.org/research-project; researcher@example.edu)'

Using a proper User-Agent helps ensure your requests are accepted and complies with Wikimedia’s usage policy.

## 🚀 Running the script

To run with the default input and output paths:

```
python script.py
```

To specify custom file paths:

```
python script.py input.csv output.csv
```

*(Adjust the script name depending on your filename.)*

# 👤 Authorship and License

This script was developed by CorraleH (https://meta.wikimedia.org/wiki/User:CorraleH).
It is released under the GNU General Public License v3.0 (GPL-3.0).
You are free to use, modify, and share this script under the terms of this license.
