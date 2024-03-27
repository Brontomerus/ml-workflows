# Unity Catalog Role
data "aws_iam_policy_document" "passrole_for_unity_catalog_external" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["arn:aws:iam::${var.aws_account_id_databricks}:role/unity-catalog-prod-UCMasterRole-${var.unity_account_policy_code}"]
      type        = "AWS"
    }
    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [var.databricks_account_id]
    }
  }
  statement {
    sid     = "ExplicitSelfRoleAssumption"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    condition {
      test     = "ArnLike"
      variable = "aws:PrincipalArn"
      values   = ["arn:aws:iam::${var.aws_account_id}:role/${local.prefix}-unitycatalog"]
    }
  }
}

resource "aws_iam_role" "external_curated_data_access_role" {
  name  = "${local.prefix}-external-curated"
  assume_role_policy = data.aws_iam_policy_document.passrole_for_unity_catalog_external.json
}


resource "aws_iam_role_policy" "external_curated_policy" {
  name   = "${local.prefix}-external-curated-policy"
  role   = aws_iam_role.external_curated_data_access_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
    {
        "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:GetLifecycleConfiguration",
            "s3:PutLifecycleConfiguration"
        ],
        "Resource": [
            "arn:aws:s3:::${aws_s3_bucket.external_curated.id}/*",
            "arn:aws:s3:::${aws_s3_bucket.external_curated.id}"
        ],
        "Effect": "Allow"
    },
    {
        "Action": [
            "kms:DescribeKey",
            "kms:GetKeyPolicy",
            "kms:GenerateDataKey",
            "kms:Encrypt",
            "kms:Decrypt"
        ],
        "Resource": "*",
        "Effect": "Allow"
    },
    {
        "Action": [
            "sts:AssumeRole"
        ],
        "Resource": [
            "arn:aws:iam::${local.account_id}:role/${local.prefix}-external-curated"
        ],
        "Effect": "Allow"
    }
    ]
  })
}

resource "aws_iam_role" "external_wrangled_data_access_role" {
  name  = "${local.prefix}-external-wrangled"
  assume_role_policy = data.aws_iam_policy_document.passrole_for_unity_catalog_external.json
}


resource "aws_iam_role_policy" "external_wrangled_policy" {
  name   = "${local.prefix}-external-wrangled-policy"
  role   = aws_iam_role.external_wrangled_data_access_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
    {
        "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:GetLifecycleConfiguration",
            "s3:PutLifecycleConfiguration",
            "kms:DescribeKey",
            "kms:GetKeyPolicy",
            "kms:GenerateDataKey",
            "kms:Encrypt",
            "kms:Decrypt"
        ],
        "Resource": [
            "arn:aws:s3:::${aws_s3_bucket.external_wrangled.id}/*",
            "arn:aws:s3:::${aws_s3_bucket.external_wrangled.id}"
        ],
        "Effect": "Allow"
    },
    {
        "Action": [
            "sts:AssumeRole"
        ],
        "Resource": [
            "arn:aws:iam::${local.account_id}:role/${local.prefix}-external-wrangled"
        ],
        "Effect": "Allow"
    }
    ]
  })
}

resource "aws_iam_role" "external_archive_data_access_role" {
  name  = "${local.prefix}-external-archive"
  assume_role_policy = data.aws_iam_policy_document.passrole_for_unity_catalog_external.json
}


resource "aws_iam_role_policy" "external_archive_policy" {
  name   = "${local.prefix}-external-archive-policy"
  role   = aws_iam_role.external_archive_data_access_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
    {
        "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:DeleteObject",
            "s3:ListBucket",
            "s3:GetBucketLocation",
            "s3:GetLifecycleConfiguration",
            "s3:PutLifecycleConfiguration"
        ],
        "Resource": [
            "arn:aws:s3:::btd-db-archive/*",
            "arn:aws:s3:::btd-db-archive"
        ],
        "Effect": "Allow"
    },
    {
        "Action": [
            "kms:DescribeKey",
            "kms:GetKeyPolicy",
            "kms:GenerateDataKey",
            "kms:Encrypt",
            "kms:Decrypt"
        ],
        "Resource": "*",
        "Effect": "Allow"
    },
    {
        "Action": [
            "sts:AssumeRole"
        ],
        "Resource": [
            "arn:aws:iam::${local.account_id}:role/${local.prefix}-external-archive"
        ],
        "Effect": "Allow"
    }
    ]
  })
}