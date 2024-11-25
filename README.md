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
The tenant must provide the 
