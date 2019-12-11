# stolen from https://www.codebyamir.com/blog/automated-ebs-snapshots-using-aws-lambda-cloudwatch
# python 3.x

# Backup all ebs volumes all regions
# Skip those volumes with tag of Backup=No

import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get list of regions
    regions = ec2.describe_regions().get('Regions',[] )

    # Iterate over regions
    for region in regions:
        print("Checking region %s " % region['RegionName'])
        reg=region['RegionName']

        # Connect to region
        ec2 = boto3.client('ec2', region_name=reg)
    
        # Get all volumes in all regions  
        result = ec2.describe_volumes()
        
        for volume in result['Volumes']:
            
            backup = 'Yes'
            
            # Get volume tag of Backup if it exists
            backup = 'Yes' #default is to backup the volume unless Backup=No tag set
            tags = volume.get('Tags', [])
            for tag in tags:
                print("tag: "+str(tag))
                if tag['Key'] == 'Backup':
                    backup = tag.get('Value')
                    
            # Skip volume if Backup tag is No
            if backup == 'No':
                continue
            
            print("Backing up %s in %s" % (volume['VolumeId'], volume['AvailabilityZone']))
        
            # Create snapshot
            result = ec2.create_snapshot(VolumeId=volume['VolumeId'],Description='Created by Lambda function ebs-backup-snapshots-create')

            # Get snapshot resource 
            ec2resource = boto3.resource('ec2', region_name=reg)
            snapshot = ec2resource.Snapshot(result['SnapshotId'])
        
            instance_name = 'N/A'
            
            # Fetch instance ID
            try: 
                instance_id = volume['Attachments'][0]['InstanceId']
            except: 
                print("no instance id; volume is presumably unattached, skip")
                #snapshot.create_tags(Tags=[{'Key': 'Name','Value': 'UNATTACHED'},{'Key': 'Origin','Value':'automated_backup'}])
                continue
                
                
            # Get instance object using ID
            result = ec2.describe_instances(InstanceIds=[instance_id])
            
            instance = result['Reservations'][0]['Instances'][0]
            
             # Find name tag for instance
            if 'Tags' in instance:
                for tags in instance['Tags']:
                    if tags["Key"] == 'Name':
                        instance_name = tags["Value"]
            
            # Add volume name to snapshot for easier identification
            snapshot.create_tags(Tags=[{'Key': 'Name','Value': instance_name}, {'Key': 'Origin','Value':'automated_backup'}])
        