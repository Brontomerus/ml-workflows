# Storage Credential and Unity Catalog IAM
data "aws_iam_policy_document" "passrole_for_storage_credential" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["arn:aws:iam::${var.aws_account_id}:role/unity-catalog-UCMasterRole"]
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
      values   = ["arn:aws:iam::${var.aws_account_id}:role/${local.prefix}-storagecredential"]
    }
  }
}

resource "aws_iam_role_policy" "storage_credential_policy" {
  name   = "${local.prefix}-storagecredential-policy"
  role   = aws_iam_role.storage_credential_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Action": [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:GetBucketLocation",
          "s3:GetLifecycleConfiguration",
        ],
        "Resource": [
          "arn:aws:s3:::${var.data_bucket}/*",
          "arn:aws:s3:::${var.data_bucket}/",
          "arn:aws:s3:::${var.curated_data_bucket}/*",
          "arn:aws:s3:::${var.curated_data_bucket}/",
          "arn:aws:s3:::${var.wrangled_data_bucket}/*",
          "arn:aws:s3:::${var.wrangled_data_bucket}/",
          "arn:aws:s3:::btd-db-archive/*",
          "arn:aws:s3:::btd-db-archive/",
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
          "arn:aws:iam::${local.account_id}:role/${local.prefix}-storagecredential"
        ],
        "Effect": "Allow"
      }
    ]
  })
}

resource "aws_iam_role" "storage_credential_role" {
  name  = "${local.prefix}-storagecredential"
  assume_role_policy = data.aws_iam_policy_document.passrole_for_storage_credential.json
}

