import aws_cdk as core
import aws_cdk.assertions as assertions

from my_alb_cdk_app.my_alb_cdk_app_stack import MyAlbCdkAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_alb_cdk_app/my_alb_cdk_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyAlbCdkAppStack(app, "my-alb-cdk-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
