## Deploy Static Sites Github Action
It's scope is to create an automatic action which enables tenants to deploy their Static Sites using S3 and CloudFront.


## Overview
The action :

- is asuming the AWS Role
- is uploading the files to an S3 bucket
- is setting the caching minimum time
- is clearing the CloudFront cache so new file versions can be retrieved


## Using This Action
The action it's capturing the esential information as input variables.

The tenant must provide the below:

|          Input            |                                            Description                                            | Required |
|:--------------------------|:--------------------------------------------------------------------------------------------------|:---------|
| assume-role-arn           | Role assumed by the action                                                                        |    Yes   |
| bucket-name               | The name of the S3 Bucket.                                                                        |    Yes   |
| working-directory         | Relative path to the folder files will be uploaded from.                                          |    Yes   |
| cloudfront-distribution   | ID Name of CloudFront Distribution.                                                               |    Yes   |
| cache-control-s-max-age   | The time period contect is chached by CloudFront for. Default is 86400 seconds (24h).             |    No    |


## Usage Example

```
      - name: Sync
        uses: UKHomeOffice/core-cloud-static-sites-action@main
        with:
          assume-role-arn: ${{ vars.role-arn }}
          cloudfront-distribution: ${{ vars.cloudfront-distribution }}
          bucket-name: ${{ vars.bucket_name }}
          working-directory: ./static-site
```

