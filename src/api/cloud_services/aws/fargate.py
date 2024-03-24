import boto3
from botocore.exceptions import ClientError

from config import aws as creds


class ECSContainerRunner:
    def __init__(self, cluster_name, task_definition, subnet_ids, security_group_ids):
        self.cluster_name = cluster_name
        self.task_definition = task_definition
        self.subnet_ids = subnet_ids
        self.security_group_ids = security_group_ids
        self.session = boto3.Session(
            aws_access_key_id=creds["aws_access_key"],
            aws_secret_access_key=creds["aws_secret_key"],
            region_name=creds["region"],
        )
        self.ecs_client = self.session.client("ecs")

    def run_container(self):
        try:
            response = self.ecs_client.run_task(
                cluster=self.cluster_name,
                launchType="FARGATE",
                taskDefinition=self.task_definition,
                count=1,
                networkConfiguration={
                    "awsvpcConfiguration": {
                        "subnets": self.subnet_ids,
                        "securityGroups": self.security_group_ids,
                        "assignPublicIp": "ENABLED",
                    }
                },
            )
            # Extract the task ARN from the response
            task_arn = response["tasks"][0]["taskArn"]
            print(f"Task started: {task_arn}")
            return task_arn
        except ClientError as e:
            print(f"An error occurred: {e}")
            return None


# Example usage:
# Ensure you replace the placeholders with your actual ECS cluster name,
# task definition ARN, subnet IDs, and security group IDs.
ecs_runner = ECSContainerRunner(
    cluster_name="your-ecs-cluster-name",
    task_definition="your-task-definition-arn",
    subnet_ids=["subnet-xxxxx", "subnet-yyyyy"],
    security_group_ids=["sg-xxxxxxx"],
)
task_arn = ecs_runner.run_container()
print(task_arn)
