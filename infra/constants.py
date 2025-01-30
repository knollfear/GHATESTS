import os

ECR_REPOSITORY = os.environ.get("ECR_REPOSITORY") or "ghatest"
REGION = os.environ.get("AWS_REGION") or "us-east-1"
ECS_CLUSTER = os.environ.get("ECS_CLUSTER") or "GHA_TEST_CLUSTER"
ECS_SERVICE = os.environ.get("ECS_SERVICE") or "ghatest_service"
ECS_TASK_DEFINITION = os.environ.get("ECS_TASK_DEFINITION") or "gha-test-task-definition"
CONTAINER_NAME = os.environ.get("CONTAINER_NAME") or "python-imagename"


# Existing resources
TARGET_GROUP_ARN = "arn:aws:elasticloadbalancing:us-east-1:040343200390:targetgroup/gha-target-group/acef878c85601adf"