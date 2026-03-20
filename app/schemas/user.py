from marshmallow import Schema, fields, validate, ValidationError



class UserSchema(Schema):
    badge_num = fields.Str(required=True, validate=validate.Regexp(r'^SHD-[A-Z]{2}[0-9]{4}$'))
    name = fields.Str(required=True, validate=validate.Regexp(r'^\w+ \w+$'))
    password = fields.Str(required=True, validate=validate.Length(min=8,max=128))