resource "aws_iam_role" "s3_instance_profile" {
  name               = "${local.prefix}-s3-instance-profile"
  description        = "Role for S3 access"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Action" : "sts:AssumeRole",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
      }
    ]
  })
  tags = merge(var.tags, {
    Name = "${local.prefix}-s3-instance-profile"
  })
}

resource "aws_iam_role_policy" "s3_instance-profile" {
  name   = "${local.prefix}-s3-instance-profile-policy"
  role   = aws_iam_role.s3_instance_profile.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        "Effect": "Allow",
        "Action": [
            "s3:ListBucket"
        ],
        "Resource": [
            "arn:aws:s3:::${var.data_bucket}",
            "arn:aws:s3:::${var.curated_data_bucket}",
            "arn:aws:s3:::${var.wrangled_data_bucket}"
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
            "s3:GetObject",
        ],
        "Resource": [
            "arn:aws:s3:::${var.data_bucket}/*",
            "arn:aws:s3:::${var.curated_data_bucket}/*",
            "arn:aws:s3:::${var.wrangled_data_bucket}/*"
        ]
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
    }
    ]
  })
}


resource "aws_iam_instance_profile" "s3_instance_profile" {
  name = "${local.prefix}-s3-instance-profile"
  role = aws_iam_role.s3_instance_profile.name
}