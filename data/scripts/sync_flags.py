import os
from pathlib import Path
import boto3
import requests
from requests.exceptions import RequestException

# Environment variable set by GitHub Actions
BUCKET_NAME = os.environ["FLAGS_BUCKET"]

# Optional local cache directory
FLAGS_DIR = Path("flags")
FLAGS_DIR.mkdir(exist_ok=True)

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

        # Download flag
        try:
            flag_response = requests.get(flag_url, timeout=30)
            flag_response.raise_for_status()

        except RequestException as e:
            print(f"Failed to fetch flag for {iso2}: {e}")
            continue

        # Save locally (optional)
        local_file = FLAGS_DIR / f"{iso2.lower()}.svg"

        with open(local_file, "wb") as f:
            f.write(flag_response.content)

        # Upload to S3
        s3_key = f"flags/{iso2.lower()}.svg"

        try:
            s3.upload_file(
                str(local_file),
                BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "ContentType": "image/svg+xml"
                }
            )

            print(f"Uploaded to s3://{BUCKET_NAME}/{s3_key}")

        except Exception as e:
            print(f"Failed to upload {iso2} to S3: {e}")
            continue

    except Exception as e:
        print(f"Unexpected error processing country record: {e}")
        continue

print("\nFlag sync complete.")
