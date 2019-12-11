
# EBS Backup Functions

Two lambda functions, ebs-backup-snapshot-create.py and ebs-backup-snapshot-cleanup.py, manage automated EBS snapshots. 


## Introduction 

ebs-backup-snapshot-create.py will find every *attached* EBS volume, in every region, and create a new snapshot of it each time it's run.  It intended to be run on a periodic schedule, which at this time is Weekly. 

ebs-backup-snapshot-cleanup.py will find all snapshots which are created by ebs-backup-snapshot-create.py (determined by a special tag) and check their create time.  Those which are older than the retention time will be deleted. It too is run on a periodic basis.  It's intended that it will be run at the same time or around the same time as create, but it is not strickly required.  

Both functions are invoked by the same Cloudwatch Event, EventDoTheBackupsPeriodically, defined in the cf.yml template.

The cf template contains everything needed for these functions to run immediately.  Except the Trigger resources (connecting the Event to the Function), which are missing.


## Dependencies
  **build.sh** assumes the following environment: 
    - bash shell at /bin/bash
    - "zip" command
    - aws cli installed (not used yet)

  The AWS lambda jobs themselves have no known dependencies.  They will, however, colide with existing lambda functions named the same thing.  


## Installation

- zip each .py file

- upload the zips to an s3 location

- update the cf definitions of the two functions with those s3 locations

- Create a Stack in the Cloudformation console or via aws cli, using the https://s3.amazonaws.com/bucketname/cf.yml notation.  


## Authors

Jared Lovell 


## Contributing

If your needs for these functions differ significantly from what is described above, it is better to fork them.
These functions make many assumptions.  Cleanup expects a certain tag set by Create, for instance.  




