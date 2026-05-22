provider "aws" {
  profile = "dev"
  region  = "us-east-1"

  default_tags {
    tags = {
      Project     = "globe-grinder"
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}