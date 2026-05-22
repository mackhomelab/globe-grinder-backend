terraform {
  required_version = "~> 1.15.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "mackhomelab-terraform-state"
    key          = "apps/globe-grinder/dev.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    profile      = "general"
  }
}