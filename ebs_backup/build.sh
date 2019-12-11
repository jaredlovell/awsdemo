#!/bin/bash

S3LOC=s3://mybucket/lambdabuilds
FUNCTIONS="ebs-backup-snapshot-cleanup ebs-backup-snapshot-create"

for f in $FUNCTIONS; do 
  zip $f.zip $f.py
  echo "aws s3 cp $f.zip $S3LOC/"
done

echo "aws s3 cp cf.yml $S3LOC/"


#deploy the whole stack is an option too
# aws --region us-west-2 cloudformation create-stack --stack-name EbsBackupLambdaFns --template-url https://s3.amazonaws.com/mybucket/lambdabuilds/cf.yml --capabilities "CAPABILITY_IAM"
