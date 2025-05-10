from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3

with Diagram("AWS Architecture Diagram", show=False):
    vpc = VPC("VPC")
    
    lb = ELB("Load Balancer")
    
    ec2_instance = EC2("EC2 Instance")
    
    database = RDS("Database")
    
    storage = S3("S3 Bucket")
    
    vpc >> lb >> ec2_instance
    ec2_instance >> database
    ec2_instance >> storage