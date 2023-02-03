from marshmallow import Schema, fields, validate
from .status_type import StatusType


class GetUserSchema(Schema):
    username = fields.Str(required=True)
    user_id = fields.Str(required=True)


class UpdateUserSchema(Schema):
    username = fields.Str(required=True)
    user_id = fields.Str(required=True)
    status = fields.Str(
        validate=validate.OneOf([StatusType.ACTIVE.value, StatusType.INACTIVE.value]),
        load_default=StatusType.INACTIVE.value,
    )


class DeleteUserSchema(Schema):
    username = fields.Str(required=True)
    user_id = fields.Str(required=True)


class StatusIndexQuerySchema(Schema):
    status = fields.Str(
        required=True,
        validate=validate.OneOf([StatusType.ACTIVE.value, StatusType.INACTIVE.value]),
    )


class CreateUserSchema(Schema):
    username = fields.Str(required=True)
    user_id = fields.Str(required=True)
    status = fields.Str(
        validate=validate.OneOf([StatusType.ACTIVE.value, StatusType.INACTIVE.value]),
        load_default=StatusType.INACTIVE.value,
    )
