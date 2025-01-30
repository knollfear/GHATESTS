import boto3
import constants


# Connectivity Check, make sure we can access AWS
sts = boto3.client("sts", region_name=constants.REGION)
account_id = sts.get_caller_identity()["Account"]

client = boto3.client('ecr', region_name=constants.REGION)

# Check for EC Repository
try:
    response = client.describe_repositories(
        registryId=account_id,
        repositoryNames=[
            constants.ECR_REPOSITORY,
        ]
    )
    print("Skipping ECR creation, ECR exists")

# Create EC Repository if it does not exist
except client.exceptions.RepositoryNotFoundException:
    response = client.create_repository(
        registryId=account_id,
        repositoryName=constants.ECR_REPOSITORY,
        imageTagMutability='MUTABLE',
        imageScanningConfiguration={
            'scanOnPush': True
        },
        encryptionConfiguration={
            'encryptionType': 'AES256',
        }
    )
    print(response)


client = boto3.client('ecs', region_name=constants.REGION)

# Check for desired Cluster Name and create it if it doesn't exist
try:
    response = client.describe_clusters(clusters=[constants.ECS_CLUSTER,])
    if len(response.get('clusters')) > 0:
        print("Skipping ECS Cluster creation, ECS Cluster exists")
    else:
        raise Exception("ECS Cluster does not exist")
except:
    response = client.create_cluster(clusterName=constants.ECS_CLUSTER,)
    print(response)

# Create ECS Service
try:
    response = client.list_services(
        cluster=constants.ECS_CLUSTER,
        launchType='FARGATE',
    )
    if len(response.get('serviceArns')) > 0:
        print("Skipping Fargate Service creation, Fargate Service exists")

    else:
        print(response)
        raise Exception("Fargate Service does not exist")
except:
    response = client.create_service(
        cluster=constants.ECS_CLUSTER,
        serviceName=constants.ECS_SERVICE,
        taskDefinition=constants.ECS_TASK_DEFINITION,
        availabilityZoneRebalancing='ENABLED',
        loadBalancers=[
            {
                'targetGroupArn': constants.TARGET_GROUP_ARN,
                'loadBalancerName': 'gha-alb',
                'containerName': constants.CONTAINER_NAME,
                'containerPort': 5001
            },
        ],
        desiredCount=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-0920a5be6b300d996', 'subnet-0f31325445bb3de91'
                ],
                'securityGroups': [
                    'sg-0aa1a6e91d036e5c0',
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
    )
    print(response)
    print("ECS Service has been created")

print("COMPLETE")

