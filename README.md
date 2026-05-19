# globe-grinder

geography-app/
│
├── infra/                        # Terraform
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf                # exports DB endpoint, S3 URLs
│   └── modules/
│       ├── database/             # Aurora Serverless
│       ├── api/                  # API Gateway + Lambda
│       └── storage/              # S3 + CloudFront
│
├── data/                         # Data pipeline
│   ├── scripts/
│   │   ├── fetch_countries.py    # pulls from REST Countries API
│   │   ├── upload_flags.py       # syncs SVGs to S3
│   │   └── sync_db.py            # upserts into Aurora
│   ├── requirements.txt
│   └── countries.json            # committed snapshot (source of truth)
│
├── api/                          # Lambda functions
│   ├── handlers/
│   │   ├── countries.py          # GET /countries
│   │   └── country.py            # GET /countries/{iso}
│   └── requirements.txt
│
├── ios/                          # Swift/Xcode project
│   └── GeographyApp.xcodeproj
│
├── web/                          # Future web client (placeholder is fine)
│   └── .gitkeep
│
└── .github/
    └── workflows/
        ├── sync-data.yml         # periodic data refresh
        └── deploy-infra.yml      # Terraform apply on merge