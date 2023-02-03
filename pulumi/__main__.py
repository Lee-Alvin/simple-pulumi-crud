"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

env = pulumi.get_stack()

users = aws.dynamodb.Table(
    "users",
    name=f"Users-{env}",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="user_id",
            type="S",
        ),
        aws.dynamodb.TableAttributeArgs(
            name="username",
            type="S",
        ),
        aws.dynamodb.TableAttributeArgs(
            name="created_date",
            type="S",
        ),
        aws.dynamodb.TableAttributeArgs(
            name="status",
            type="S",
        ),
    ],
    global_secondary_indexes=[
        aws.dynamodb.TableGlobalSecondaryIndexArgs(
            hash_key="status", projection_type="ALL", name="StatusIndex"
        ),
        aws.dynamodb.TableGlobalSecondaryIndexArgs(
            hash_key="status",
            range_key="created_date",
            projection_type="ALL",
            name="StatusCreatedDateIndex",
        ),
    ],
    billing_mode="PAY_PER_REQUEST",
    hash_key="user_id",
    range_key="username",
)

pulumi.export("users", users)
