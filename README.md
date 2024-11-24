## Deploy Static Sites Github Action
It's scope is to create an automatic action which enables tenants to deploy their Static Sites using S3 and CloudFront.


## Overview
The action :

- is asuming the AWS Role
- is uploading the files to an S3 bucket
- is setting the caching minimum time
- is clearing the CloudFront cache so new file versions can be retrieved


## Usage
The action it's capturing the esential information as input variables.

The tenant must provide the below:

|          Input            |                                            Description                                            | Required |
|:--------------------------|:--------------------------------------------------------------------------------------------------|:---------|
| assume-role-arn           | Role assumed by the action                                                                        |    Yes   |
| bucket-name               | The name of the S3 Bucket.                                                                        |    Yes   |
| working-directory         | Folder the files will be synced from.                                                             |    Yes   |
| cache-control-s-max-age   | The time period contect is chached by CloudFront for. Default is 86400 seconds (24h).             |    No    |
| cloudfront-distribution   | ID Name of CloudFront Distribution.                                                               |    No    |


