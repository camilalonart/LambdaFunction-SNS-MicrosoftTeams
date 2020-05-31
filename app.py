import boto3
from django.db import models

client = boto3.client(
    'sns',
    aws_access_key_id="YOUR ACCES KEY",
    aws_secret_access_key="YOUR SECRET KEY",
    region_name="us-east-1")


class Pedido(models.Model):

    response = client.add_permission(
        TopicArn='arn:aws:sns:us-east-1:845355343352:totoro',
        Label='__default_policy_ID',
        AWSAccountId=[
            '8453-5534-3352',
        ],
        ActionName=[
            "SNS:Publish",
            "SNS:RemovePermission",
            "SNS:SetTopicAttributes",
            "SNS:DeleteTopic",
            "SNS:ListSubscriptionsByTopic"
        ]
    )


    response = client.publish(
        Message="El pedido se encuentra ",
        Subject="Id pedido",

    )

    print("Response: {}".format(response))