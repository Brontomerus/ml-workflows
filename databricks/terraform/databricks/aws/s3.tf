# DBFS Root
resource "aws_s3_bucket" "root_storage_bucket" {
  bucket        = local.dbfsname
  force_destroy = true
  tags          = merge(var.tags, {
    Name        = local.dbfsname
  })
}

resource "aws_s3_bucket_acl" "root_bucket_acls" {
  bucket        = aws_s3_bucket.root_storage_bucket.id
  acl           = "private"
}

resource "aws_s3_bucket_versioning" "root_bucket_versioning" {
  bucket        =  aws_s3_bucket.root_storage_bucket.id
  versioning_configuration {
    status      = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "root_storage_bucket" {
  bucket        = aws_s3_bucket.root_storage_bucket.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "root_storage_bucket" {
  bucket                  = aws_s3_bucket.root_storage_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on              = [aws_s3_bucket.root_storage_bucket]
}

data "databricks_aws_bucket_policy" "this" {
  bucket        = aws_s3_bucket.root_storage_bucket.bucket
}

resource "aws_s3_bucket_policy" "root_bucket_policy" {
  bucket        = aws_s3_bucket.root_storage_bucket.id
  policy        = data.databricks_aws_bucket_policy.this.json
  depends_on    = [aws_s3_bucket_public_access_block.root_storage_bucket]
}

# Unity Catalog S3
resource "aws_s3_bucket" "unity_catalog_bucket" {
  bucket        = local.ucname
  force_destroy = true
  tags          = merge(var.tags, {
    Name        = local.ucname
  })
}

resource "aws_s3_bucket_acl" "unity_catalog_acls" {
  bucket        = aws_s3_bucket.unity_catalog_bucket.id
  acl           = "private"
}

resource "aws_s3_bucket_versioning" "unity_catalog_versioning" {
  bucket        = aws_s3_bucket.unity_catalog_bucket.id
  versioning_configuration {
    status      = "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "unity_catalog" {
  bucket        = aws_s3_bucket.unity_catalog_bucket.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "unity_catalog" {
  bucket                  = aws_s3_bucket.unity_catalog_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on              = [aws_s3_bucket.unity_catalog_bucket]
}

# External Tables: Curated
resource "aws_s3_bucket" "external_curated" {
  bucket        = var.curated_data_bucket
  force_destroy = true
  tags          = merge(var.tags, {
    Name        = var.curated_data_bucket
  })
}

resource "aws_s3_bucket_acl" "external_curated_acls" {
  bucket        = aws_s3_bucket.external_curated.id
  acl           = "private"
}

# resource "aws_s3_bucket_versioning" "external_curated_versioning" {
#   bucket        =  aws_s3_bucket.external_curated.id
#   versioning_configuration {
#     status      = "Enabled"
#   }
# }

resource "aws_s3_bucket_server_side_encryption_configuration" "external_curated" {
  bucket        = aws_s3_bucket.external_curated.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "external_curated" {
  bucket                  = aws_s3_bucket.external_curated.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on              = [aws_s3_bucket.external_curated]
}

data "databricks_aws_bucket_policy" "external_curated" {
  bucket        = aws_s3_bucket.external_curated.bucket
}

resource "aws_s3_bucket_policy" "external_curated_policy" {
  bucket        = aws_s3_bucket.external_curated.id
  policy        = data.databricks_aws_bucket_policy.external_curated.json
  depends_on    = [aws_s3_bucket_public_access_block.external_curated]
}






# External Tables: Wrang;ed
resource "aws_s3_bucket" "external_wrangled" {
  bucket        = var.wrangled_data_bucket
  force_destroy = true
  tags          = merge(var.tags, {
    Name        = var.wrangled_data_bucket
  })
}

resource "aws_s3_bucket_acl" "external_wrangled_acls" {
  bucket        = aws_s3_bucket.external_wrangled.id
  acl           = "private"
}

# resource "aws_s3_bucket_versioning" "external_wrangled_versioning" {
#   bucket        =  aws_s3_bucket.external_wrangled.id
#   versioning_configuration {
#     status      = "Enabled"
#   }
# }

resource "aws_s3_bucket_server_side_encryption_configuration" "external_wrangled" {
  bucket        = aws_s3_bucket.external_wrangled.bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "external_wrangled" {
  bucket                  = aws_s3_bucket.external_wrangled.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
  depends_on              = [aws_s3_bucket.external_wrangled]
}

data "databricks_aws_bucket_policy" "external_wrangled" {
  bucket        = aws_s3_bucket.external_wrangled.bucket
}

resource "aws_s3_bucket_policy" "external_wrangled_policy" {
  bucket        = aws_s3_bucket.external_wrangled.id
  policy        = data.databricks_aws_bucket_policy.external_wrangled.json
  depends_on    = [aws_s3_bucket_public_access_block.external_wrangled]
}