#!/usr/bin/env python

# Requirements:
# pip install boto
import boto
import boto.s3.connection
import os
import sys
import uuid
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Get access key and secret key from credentials file
from credentials import *

# Get the file to upload
from pdb import set_trace as stp

# Create a connection to the S3 service.
conn = boto.connect_s3(
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        host = 's3.amazonaws.com',
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

print("Connection to S3 established")
for bucket in conn.get_all_buckets():
    print("{name}\t{created}".format(
        name = bucket.name,
        created = bucket.creation_date,
        ))
print("\n")

print("Creating bucket")
bucket_id = gen_id()
bucket = conn.create_bucket(bucket_id)

print("reading local file")
for root, dirs, files in os.walk("."):
    for file in files:
        if file_name.startswith("2022"):
            key = bucket.new_key(gen_id + ".png")
            key.set_contents_from_filename(file_name)
            key.set_acl('public-read')
            print("File uploaded to S3")

print("what files were created there?")
print("(need to delete everything before continuing otherwise I get a 409 conflict error)")
for key in bucket.list():
    print("{name}\t{size}\t{modified}".format(
            name = key.name,
            size = key.size,
            modified = key.last_modified,
    ))
    new_filename = "downloaded." + gen_id() + ".png"

    print("downloading to " + new_filename)
    sub_key = bucket.get_key(key.name)
    sub_key.get_contents_to_filename(new_filename)

    bucket.delete_key(key.name)

print("now deleting the bucket.")
conn.delete_bucket(bucket.name)

print("done")