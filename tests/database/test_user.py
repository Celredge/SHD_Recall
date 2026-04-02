import pytest
from sqlalchemy import create_engine, Column, Integer, String
from datetime import datetime
from app.database import db
from app.models.user import User
from app.schemas.user import UserSchema
from marshmallow import ValidationError

#-------------
#Fixtures
#-------------

@pytest.fixture
def schema():
    return UserSchema()

@pytest.fixture
def valid_user_dict():
    return  {
    "badge_num": "SHD-AB1234",       # Matches regex r'^SHD-[A-Z]{2}[0-9]{4}$'
    "name": "John Doe",               # Matches regex r'^\w+ \w+$'
    "password": "password123",        # Length between 8-128
    "status": "Online",               # One of ["Online", "Offline", "Away"]
    "latitude": 40.7128,              # Between -90 and 90
    "longitude": -74.0060             # Between -180 and 180
    }

EDGE_CASES_BADGENUM = {
    ("badge_num", ""),
    ("badge_num", "SHD-AB123"),
    ("badge_num", "sHD-ABC1234"),
    ("badge_num", "SHD-ab1234"),
    ("badge_num", "SHD-AB12X4"),
    ("badge_num", "XYZ-AB1234"),
    ("badge_num", "SHDAB1234"),
    ("badge_num", "SHD_AB1234"),
    ("badge_num", "SHD-AB 1234"),
    ("badge_num", " SHD-AB0000"),
    ("badge_num", "SHD-AB0000 "),
    ("badge_num", "SHD-AB 0000")
}

EDGE_CASES_BADGENUM_VALID = {
    ("badge_num", "SHD-XY9999"),
    ("badge_num", "SHD-ZZ0000"),
    ("badge_num", "SHD-AA1234"),
}
#-------------
#Schema Load Tests
#-------------

    #-----------------
    #Badge_Number Tests
    #-----------------


@pytest.mark.parametrize("field, value", EDGE_CASES_BADGENUM_VALID)
def test_valid_badge_num(schema, valid_user_dict,field,value):
    valid_user_dict[field] = value

    try:
        result = schema.load(valid_user_dict)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid badge_num '{value}': {excinfo}")

@pytest.mark.parametrize("field, value", EDGE_CASES_BADGENUM)
def test_invalid_badge_num_empty(schema,valid_user_dict,field,value):
    valid_user_dict[field] = value
    
    with pytest.raises(ValidationError) as excinfo:
        schema.load(valid_user_dict)
    
    assert field in excinfo.value.messages

        
    

    








