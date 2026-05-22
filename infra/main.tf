module "flags_storage" {
  source = "./modules/storage"

  bucket_name = var.flags_bucket_name
}

