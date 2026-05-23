import os
from pathlib import Path
import json
import boto3
import requests
from requests.exceptions import RequestException

# Environment variable set by GitHub Actions
BUCKET_NAME = os.environ["FLAGS_BUCKET"]

# Optional local cache directory
FLAGS_DIR = Path("flags")
FLAGS_DIR.mkdir(exist_ok=True)

BUILD_DIR = Path("build")
BUILD_DIR.mkdir(exist_ok=True)

COUNTRIES_JSON = BUILD_DIR / "countries.json"

# AWS S3 client
s3 = boto3.client("s3")

# REST Countries API
url = "https://restcountries.com/v3.1/all?fields=cca2,cca3,name,capital,languages,latlng"

response = requests.get(url, timeout=30)
response.raise_for_status()

countries = response.json()

# Final normalized dataset
country_data = []

for c in countries:
    try:
        iso2 = c["cca2"]
        iso3 = c.get("cca3")
        name = c["name"]["common"]

        capital = (c.get("capital") or [None])[0]
        languages = list(c.get("languages", {}).values())
        lat, lng = c.get("latlng", [None, None])

        flag_url = f"https://flagcdn.com/{iso2.lower()}.svg"

        print(f"\nProcessing {name} ({iso2})")
        print(f"Fetching: {flag_url}")
        
        # Build country entry for our dataset
        country_entry = {
            "iso2": iso2,
            "iso3": iso3,
            "name": name,
            "capital": capital,
            "languages": languages,
            "latitude": lat,
            "longitude": lng
        }

        country_data.append(country_entry)

    except Exception as e:
        print(f"Unexpected error processing country record: {e}")
        continue

# Sort alphabetically
country_data.sort(key=lambda x: x["name"])

# Save countries.json locally
with open(COUNTRIES_JSON, "w", encoding="utf-8") as f:
    json.dump(country_data, f, ensure_ascii=False, indent=2)

print(f"Saved countries JSON to {COUNTRIES_JSON}")

# Upload countries.json to S3
try:
    s3.upload_file(
        str(COUNTRIES_JSON),
        BUCKET_NAME,
        "countries/countries.json",
        ExtraArgs={
            "ContentType": "application/json"
        }
    )

    print(
        f"Uploaded countries JSON to "
        f"s3://{BUCKET_NAME}/countries/countries.json"
    )

except Exception as e:
    print(f"Failed to upload countries.json: {e}")

print("\nCountry + flag sync complete.")