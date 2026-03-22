from marshmallow import Schema, fields, validate, ValidationError



class UserSchema(Schema):
    """A Schema that allows Marshmallow to validate the User Model.
        This ensures that the data being sent to the backend is in the correct format and meets the requirements of the User Model.

    Args:
        Schema (Marshmallow.Schema): The base class for all Marshmallow Schemas.
    """
    badge_num = fields.Str(required=True, validate=validate.Regexp(r'^SHD-[A-Z]{2}[0-9]{4}$'))
    name = fields.Str(required=True, validate=validate.Regexp(r'^\w+ \w+$'))
    password = fields.Str(required=True, validate=validate.Length(min=8,max=128))