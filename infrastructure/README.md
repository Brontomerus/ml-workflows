# Infrastructure

# Getting Started

Make sure you have awscli installed and if you have not yet configured your AWS SDK, then run and fill out the required fields:

```bash
$ pip install awscli
...
$ aws configure
AWS Access Key ID [None]: <your access key id here>
AWS Secret Access Key [None]: <your secret key here>
Default region name [None]: us-east-2
Default output format [None]: json
```

If you have multiple AWS profiles (like me), then you'll need to whip up a quick environment variable to avoid messing up and throwing this into the wrong AWS Account... which would __not__ be ideal:
```bash
$ export AWS_PROFILES=my-profile-name
```
