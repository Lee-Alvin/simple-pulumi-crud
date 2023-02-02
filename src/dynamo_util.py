import boto3
import os
import json
import logging
import datetime

from marshmallow.exceptions import ValidationError
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from typing import Union

from models.request import (
    GetUserSchema,
    CreateUserSchema,
    DeleteUserSchema,
    UpdateUserSchema,
    StatusIndexQuerySchema,
)
from models.response import APIResponse

USERS_TABLE_NAME = os.getenv("USERS_TABLE_NAME") or "Users-dev"
STATUS_INDEX_NAME = os.getenv("STATUS_INDEX_NAME") or "StatusIndex"

logger = logging.getLogger(__name__)
dynamo = boto3.resource("dynamodb")
table = dynamo.Table(USERS_TABLE_NAME)
table.load()


def delete_user(request_body: Union[dict, str]):
    try:
        DeleteUserSchema().loads(json.dumps(request_body))

        response = table.delete_item(
            Key={
                "username": request_body["username"],
                "user_id": request_body["user_id"],
            },
            ReturnValues="ALL_OLD",
        )

        return APIResponse(
            code="Success",
            message="Success",
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            operation="delete_item",
            body=response["Attributes"]
            if "Attributes" in response
            else "No items matched. No items deleted.",
        ).return_JSON()
    except ClientError as e:
        logger.error(
            f"Failed to delete_item on {USERS_TABLE_NAME}. Code: {e.response['Error']['Code']}. Message: {e.response['Error']['Message']}"
        )

        return APIResponse(
            code=e.response["Error"]["Code"],
            message=e.response["Error"]["Message"],
            http_status_code=500,
            operation=e.operation_name,
            body="",
        ).return_JSON()
    except ValidationError as e:
        logger.error(f"Failed API request validator")
        return APIResponse(
            code="ValidationError",
            message="Failed API request validator",
            http_status_code=400,
            operation="delete_item",
            body=str(e),
        ).return_JSON()


def index_query(request_body: Union[dict, str]):
    try:
        request_body = StatusIndexQuerySchema().loads(json.dumps(request_body))
        response = table.query(
            IndexName=STATUS_INDEX_NAME,
            KeyConditionExpression=Key("status").eq(request_body["status"]),
        )

        return APIResponse(
            code="Success",
            message="Success",
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            operation="query",
            body={"Count": response["Count"], "Items": response["Items"]}
            if "Items" in response
            else "",
        ).return_JSON()

    except ClientError as e:
        logger.error(
            f"Failed to query {STATUS_INDEX_NAME} on {USERS_TABLE_NAME}. Code: {e.response['Error']['Code']}. Message: {e.response['Error']['Message']}"
        )

        return APIResponse(
            code=e.response["Error"]["Code"],
            message=e.response["Error"]["Message"],
            http_status_code=500,
            operation=e.operation_name,
            body="",
        ).return_JSON()

    except ValidationError as e:
        logger.error(f"Failed API request validator")
        return APIResponse(
            code="ValidationError",
            message="Failed API request validator",
            http_status_code=400,
            operation="query",
            body=str(e),
        ).return_JSON()


def create_user(request_body: Union[dict, str]):
    try:
        request_body = CreateUserSchema().loads(json.dumps(request_body))
        response = table.put_item(
            Item={
                "username": request_body["username"],
                "user_id": request_body["user_id"],
                "status": request_body["status"],
                "created_date": datetime.datetime.now().strftime("%x"),
            },
        )

        return APIResponse(
            code="Success",
            message="Success",
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            operation="create_item",
            body="",
        ).return_JSON()
    except ClientError as e:
        logger.error(
            f"Failed to create_item on {USERS_TABLE_NAME}. Code: {e.response['Error']['Code']}. Message: {e.response['Error']['Message']}"
        )

        return APIResponse(
            code=e.response["Error"]["Code"],
            message=e.response["Error"]["Message"],
            http_status_code=500,
            operation=e.operation_name,
            body="",
        ).return_JSON()
    except ValidationError as e:
        logger.error(f"Failed API request validator")
        return APIResponse(
            code="ValidationError",
            message="Failed API request validator",
            http_status_code=400,
            operation="create_item",
            body=str(e),
        ).return_JSON()


def update_user(request_body: Union[dict, str]):
    try:
        request_body = UpdateUserSchema().loads(json.dumps(request_body))
        response = table.update_item(
            Key={
                "username": request_body["username"],
                "user_id": request_body["user_id"],
            },
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": request_body["status"]},
            ReturnValues="ALL_NEW",
        )

        return APIResponse(
            code="Success",
            message="Success",
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            operation="update_item",
            body=response["Attributes"],
        ).return_JSON()
    except ClientError as e:
        logger.error(
            f"Failed to update_item on {USERS_TABLE_NAME}. Code: {e.response['Error']['Code']}. Message: {e.response['Error']['Message']}"
        )

        return APIResponse(
            code=e.response["Error"]["Code"],
            message=e.response["Error"]["Message"],
            http_status_code=500,
            operation=e.operation_name,
            body="",
        ).return_JSON()
    except ValidationError as e:
        logger.error(f"Failed API request validator")
        return APIResponse(
            code="ValidationError",
            message="Failed API request validator",
            http_status_code=400,
            operation="update_item",
            body=str(e),
        ).return_JSON()


def get_user(request_body: Union[dict, str]):
    try:
        request_body = GetUserSchema().loads(json.dumps(request_body))
        response = table.get_item(
            Key={
                "username": request_body["username"],
                "user_id": request_body["user_id"],
            }
        )

        return APIResponse(
            code="Success",
            message="Success",
            http_status_code=response["ResponseMetadata"]["HTTPStatusCode"],
            operation="get_item",
            body=response["Item"] if "Item" in response else "",
        ).return_JSON()

    except ClientError as e:
        logger.error(
            f"Failed to get_item on {USERS_TABLE_NAME}. Code: {e.response['Error']['Code']}. Message: {e.response['Error']['Message']}"
        )

        return APIResponse(
            code=e.response["Error"]["Code"],
            message=e.response["Error"]["Message"],
            http_status_code=500,
            operation=e.operation_name,
            body="",
        ).return_JSON()

    except ValidationError as e:
        logger.error(f"Failed API request validator")
        return APIResponse(
            code="ValidationError",
            message="Failed API request validator",
            http_status_code=400,
            operation="get_item",
            body=str(e),
        ).return_JSON()
