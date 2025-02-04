import json
import boto3
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy,
)
from constructs import Construct


def get_latest_ecr_image_tag(repository_name: str, region: str) -> str:
    """
    Retrieve the latest image tag from an ECR repository.
    """
    ecr_client = boto3.client("ecr", region_name=region)
    response = ecr_client.describe_images(
        repositoryName=repository_name,
    )
    if not response["imageDetails"]:
        raise ValueError(f"No images found in ECR repository: {repository_name}")
    sortedDetails = response["imageDetails"]
    sortedDetails.sort(key=lambda x: x["imagePushedAt"])
    return sortedDetails[-1]["imageTags"][0]


class MyAlbCdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Load the JSON task definition
        with open("../infra/task-definition.json", "r") as file:
            task_definition_json = json.load(file)

        # Create a VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)

        # Create a security group for the ECS cluster
        ecs_security_group = ec2.SecurityGroup(
            self, "EcsSecurityGroup",
            vpc=vpc,
            description="Security group for ECS tasks",
            allow_all_outbound=True,
        )

        # Create a security group for the RDS instance
        rds_security_group = ec2.SecurityGroup(
            self, "RdsSecurityGroup",
            vpc=vpc,
            description="Security group for Aurora PostgreSQL",
            allow_all_outbound=True,
        )

        # Allow ECS tasks to access the RDS instance
        rds_security_group.add_ingress_rule(
            peer=ecs_security_group,
            connection=ec2.Port.tcp(5432),  # PostgreSQL port
            description="Allow inbound from ECS tasks",
        )

        # Create an Aurora PostgreSQL cluster
        db_cluster = rds.DatabaseCluster(
            self, "MyAuroraCluster",
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_15_3  # Specify your desired version
            ),
            credentials=rds.Credentials.from_generated_secret("postgres"),  # Generate a secret for the master user
            instance_props=rds.InstanceProps(
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                security_groups=[rds_security_group],
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MEDIUM),
            ),
            default_database_name="mydatabase",  # Optional: Specify a default database name
            removal_policy=RemovalPolicy.DESTROY,  # Optional: Adjust removal policy as needed
        )

        # Create an ECS Fargate Cluster
        cluster = ecs.Cluster(self, "MyFargateCluster", vpc=vpc)

        # Create a Fargate Task Definition
        task_definition = ecs.FargateTaskDefinition(
            self, "MyTaskDefinition",
            cpu=task_definition_json["cpu"],
            memory_limit_mib=task_definition_json["memory"],
            execution_role=iam.Role.from_role_arn(
                self, "ExecutionRole",
                role_arn=task_definition_json["executionRoleArn"]
            )
        )

        image_tag = get_latest_ecr_image_tag("ghatest", "us-east-1")
        print(image_tag)

        # Add the container to the task definition
        container_definition = task_definition_json["containerDefinitions"][0]
        container = task_definition.add_container(
            container_definition["name"],
            image=ecs.ContainerImage.from_registry(container_definition["image"].replace("latest", image_tag)),
            port_mappings=[ecs.PortMapping(
                container_port=port_mapping["containerPort"],
                host_port=port_mapping["hostPort"],
                protocol=ecs.Protocol.TCP
            ) for port_mapping in container_definition["portMappings"]],
            environment={
                env["name"]: env["value"]
                for env in container_definition["environment"]
            }
        )

        # Add the RDS endpoint and credentials to the container environment
        container.add_environment("DB_HOST", db_cluster.cluster_endpoint.hostname)
        container.add_environment("DB_PORT", "5432")
        container.add_environment("DB_NAME", "mydatabase")
        container.add_environment("DB_USER", "postgres")  # Use the master username
        container.add_secret("DB_PASSWORD", ecs.Secret.from_secrets_manager(db_cluster.secret, "password"))

        # Create a Fargate service
        fargate_service = ecs.FargateService(
            self, "MyFargateService",
            cluster=cluster,
            task_definition=task_definition,
            assign_public_ip=True,  # Assign public IP if needed
            desired_count=1,  # Number of tasks to run
        )

        # Create an Application Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self, "MyALB",
            vpc=vpc,
            internet_facing=True,
        )

        # Add a listener to the ALB
        listener = alb.add_listener("MyListener", port=80)

        # Add a target group and associate it with the Fargate service
        target_group = listener.add_targets(
            "MyTargetGroup",
            port=80,
            targets=[fargate_service],
        )

        # Output the ALB DNS name
        self.alb_dns_name = alb.load_balancer_dns_name

        # Output the RDS endpoint
        self.rds_endpoint = db_cluster.cluster_endpoint.hostname