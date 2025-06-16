# Author: CorraleH (https://meta.wikimedia.org/wiki/User:CorraleH)
# License: GNU General Public License v3.0 (https://www.gnu.org/licenses/gpl-3.0.en.html)

import pandas as pd
import requests
import time
from requests.exceptions import RequestException, JSONDecodeError, HTTPError

def check_wikidata_presence(name, language='en'):
    """
    Checks if there is an item in Wikidata with the given name.
    Implements exponential backoff to handle 429 errors (rate limits).
    Change the language variable to your preferred language.
    """
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbsearchentities',
        'search': name,
        'language': language,
        'format': 'json',
        'limit': 1
    }

    """
    IMPORTANT: The Wikimedia API requires a descriptive 'User-Agent' header for all requests.
    You should replace the value below with your own script name, version, project URL, or contact email.
    Example format: 'User-Agent': 'MyScript/1.0 (https://example.org/research-project; researcher@example.edu)'
    """
    headers = {
        'User-Agent': 'MyScript/1.0 (https://example.org/research-project; researcher@example.edu)'
    }

    max_retries = 3  # Maximum number of retries on failure
    backoff_factor = 2  # Exponential backoff factor
    timeout = 10  # Request timeout in seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()

            if not response.text.strip():
                print(f"⚠️  Empty response for '{name}'")
                return False

            data = response.json()
            return bool(data.get('search'))

        except HTTPError as err:
            # Handle rate limiting by waiting before retrying
            if err.response.status_code == 429:
                wait_time = backoff_factor ** attempt
                print(f"⏳ Rate limited for '{name}'. Attempt {attempt+1}/{max_retries}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            print(f"❌ HTTP error for '{name}': {err}")
            return False

        except (RequestException, JSONDecodeError) as err:
            print(f"❌ Request failed for '{name}': {err}")
            return False

    print(f"❌ Failed after {max_retries} attempts for '{name}'")
    return False

def main(csv_input_path='names_titles.csv', csv_output_path='researchers_not_found_wikidata.csv'):
    """
    Reads a CSV file containing researcher names, checks their presence in Wikidata,
    and outputs the names not found to another CSV file.
    """
    try:
        df = pd.read_csv(csv_input_path)
    except FileNotFoundError:
        print(f"❌ File not found: {csv_input_path}")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    if 'name' not in df.columns:
        print("❌ CSV must contain a 'name' column")
        return

    not_found = []
    total_names = len(df)

    print(f"🔍 Checking {total_names} names against Wikidata...")

    for i, name in enumerate(df['name']):
        if not pd.isna(name) and name.strip():
            if not check_wikidata_presence(name):
                not_found.append(name)

            # Show progress every 10 names
            if (i + 1) % 10 == 0 or (i + 1) == total_names:
                print(f"📊 Progress: {i+1}/{total_names} | Not found: {len(not_found)}")

            # Wait 1 second between requests
            time.sleep(1)
        else:
            print(f"⚠️  Skipping empty name at row {i}")

    results_df = pd.DataFrame({'name_not_found': not_found})

    try:
        results_df.to_csv(csv_output_path, index=False)
        print(f"✅ Results saved to {csv_output_path}")
        print(f"\n📝 Summary:")
        print(f"Total names checked: {total_names}")
        print(f"Names not found in Wikidata: {len(not_found)}")

    except Exception as e:
        print(f"❌ Error saving results: {e}")

if __name__ == '__main__':
    main()
