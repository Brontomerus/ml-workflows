# Unity Catalog Role
data "aws_iam_policy_document" "passrole_for_unity_catalog" {
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

resource "aws_iam_role" "unity_catalog_role" {
  name  = "${local.prefix}-unitycatalog"
  assume_role_policy = data.aws_iam_policy_document.passrole_for_unity_catalog.json
}


resource "aws_iam_role_policy" "unity_catalog" {
  name   = "${local.prefix}-unitycatalog-policy"
  role   = aws_iam_role.unity_catalog_role.id
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
            "arn:aws:s3:::${aws_s3_bucket.unity_catalog_bucket.id}/*",
            "arn:aws:s3:::${aws_s3_bucket.unity_catalog_bucket.id}"
        ],
        "Effect": "Allow"
    },
    {
        "Action": [
            "sts:AssumeRole"
        ],
        "Resource": [
            "arn:aws:iam::${local.account_id}:role/${local.prefix}-unitycatalog"
        ],
        "Effect": "Allow"
    }
    ]
  })
}