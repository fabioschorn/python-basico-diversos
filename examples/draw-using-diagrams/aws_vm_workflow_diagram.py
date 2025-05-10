from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users, Client
from diagrams.onprem.network import Internet

with Diagram("AWS Vulnerability Management Workflow", show=False, direction="LR"):

    # External sources
    qualys = Internet("Qualys Cloud")
    team = Users("Security Team")

    # S3 input
    s3 = S3("qualys-report.csv")

    # Lambda function group
    with Cluster("Lambda Functions"):
        lambda_parse = Lambda("Parse & Filter CSV")
        lambda_diff = Lambda("Detect New QIDs")
        lambda_ticket = Lambda("Generate Jira Tickets")
        lambda_update = Lambda("Update Jira + DB")

    # Database Layer
    with Cluster("Database Layer"):
        rds = RDSPostgresqlInstance("PostgreSQL\nVuln DB")

    # Messaging/Monitoring/Integration
    sns = SNS("SNS Notification")
    sqs = SQS("Ticket Queue (SQS)")
    cloudwatch = Cloudwatch("CloudWatch Logs")
    api = APIGateway("Optional API")

    # Jira integration (using a generic on-prem icon)
    jira = Client("JIRA Ticketing")

    # Flow connections
    qualys >> s3 >> lambda_parse >> lambda_diff
    lambda_parse >> sns >> team
    lambda_diff >> lambda_ticket >> [jira, sqs]
    lambda_ticket >> lambda_update >> [rds, jira, cloudwatch]
    lambda_update >> cloudwatch >> team
    api >> team
    lambda_parse >> rds