import json
import os
from pathlib import Path

import boto3
import requests

BUCKET_NAME = os.environ["FLAGS_BUCKET"]

RAW_DIR = Path("geojson/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "datasets/geo-countries/master/"
    "data/countries.geojson"
)

OUTPUT_FILE = RAW_DIR / "countries.geojson"

print("Downloading GeoJSON dataset...")

response = requests.get(GEOJSON_URL, timeout=60)
response.raise_for_status()

with open(OUTPUT_FILE, "wb") as f:
    f.write(response.content)

print(f"Saved GeoJSON dataset to {OUTPUT_FILE}")

#
# Load dataset
#
with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

#
# Upload master file
#
s3 = boto3.client("s3")

s3.upload_file(
    str(OUTPUT_FILE),
    BUCKET_NAME,
    "geojson/countries.geojson",
    ExtraArgs={
        "ContentType": "application/geo+json"
    }
)

print(
    f"Uploaded to s3://{BUCKET_NAME}/geojson/countries.geojson"
)