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
    "password": "Password123!",        # Length between 8-128
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
    ("badge_num", "SHD-AB 0000"),
    ("badge_num", ""),
    ("badge_num", 2.4),
    ("badge_num", 1),
    ("badge_num", "shd-AB0000"),

}

EDGE_CASES_BADGENUM_VALID = {
    ("badge_num", "SHD-XY9999"),
    ("badge_num", "SHD-ZZ0000"),
    ("badge_num", "SHD-AA1234"),
}

EDGE_CASES_NAME = {
    ("name", ""),                    # empty string
    ("name", "John"),                # single word
    ("name", "John  Doe"),           # double space
    ("name", " John Doe"),           # leading space
    ("name", "John Doe "),           # trailing space
    ("name", "John_Doe"),            # underscore instead of space
    ("name", "John-Doe"),            # hyphen (not allowed by \w)
    ("name", "John Doe Smith"),      # too many words
    ("name", 123),                   # not a string
    ("name", None),                  # None
    ("name", "___ ___"),            # only underscores
    ("name", "123 456"),            # only numbers (allowed by \w but should fail due to regex)
}

EDGE_CASES_NAME_VALID = {
    ("name", "Jane Smith"),
    ("name", "Alice Johnson"),
    ("name", "Bob Brown"),
    ("name", "A B"),                 # minimal valid case
    ("name", "John1 Doe2"),
    }          # numbers allowed by \w

EDGE_CASES_PASSWORD_VALID = {
    ("password", "Password1!"),
    ("password", "A1b@5678"),
    ("password", "Complex#Pass123"),
}

EDGE_CASES_PASSWORD = {
    ("password", "short1!"),          # too short
    ("password", "alllowercase1!"),   # no uppercase
    ("password", "ALLUPPERCASE1!"),   # no lowercase
    ("password", "NoNumber!"),        # no digit
    ("password", "NoSpecial1"),       # no special char
    ("password", "12345678!"),        # no letters
    ("password", "Password!"),        # no number
    ("password", ""),                 # empty
    ("password", None),               # None
}

EDGE_CASES_LONGITUDE = {
    ("longitude", -180.1),
    ("longitude", 180.1),
    ("longitude", "west"),
    ("longitude", None),
}

EDGE_CASES_LONGITUDE_VALID = {
    ("longitude", -180.0),
    ("longitude", 180.0),
    ("longitude", 0.0),
    ("longitude", 45.1234),
    ("longitude", -45.1234),
}

EDGE_CASES_LATITUDE_VALID = {
    ("latitude", -90.0),
    ("latitude", 90.0),
    ("latitude", 0.0),
    ("latitude", 45.1234),
    ("latitude", -45.1234),
}

EDGE_CASES_LATITUDE ={
    ("latitude", -90.1),
    ("latitude", 90.1),
    ("latitude", "north"),
    ("latitude", None),
}

EDGE_CASES_STATUS = {
    ("status", "Busy"),
    ("status", "online"),  # case-sensitive
    ("status", "OFFLINE"), # case-sensitive
    ("status", "Away "),   # trailing space
    ("status", " Away"),   # leading space
    ("status", ""),        # empty string
    ("status", None),      # None
}

EDGE_CASES_STATUS_VALID = {
    ("status", "Online"),
    ("status", "Offline"),
    ("status", "Away"),
}

#-------------
#Schema Load Tests
#-------------

    #-----------------
    #Badge_Number Tests
    #-----------------


@pytest.mark.parametrize("field, value", EDGE_CASES_BADGENUM_VALID)
def test_valid_badge_num(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value

    try:
        result = schema.load(cop)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid badge_num '{value}': {excinfo}")

@pytest.mark.parametrize("field, value", EDGE_CASES_BADGENUM)
def test_invalid_badge_num_empty(schema,valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value
    
    with pytest.raises(ValidationError) as excinfo:
        schema.load(cop)
    
    assert field in excinfo.value.messages

        
    #-----------------
    #Name Tests
    #-----------------

  
@pytest.mark.parametrize("field, value", EDGE_CASES_NAME_VALID)
def test_valid_name(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value

    try:
        result = schema.load(cop)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid name '{value}': {excinfo}")
    
@pytest.mark.parametrize("field, value", EDGE_CASES_NAME)
def test_invalid_name(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value
        
    with pytest.raises(ValidationError) as excinfo:
        schema.load(cop)
        
    assert field in excinfo.value.messages
    
    
    #-----------------
    #Raw Password Tests
    #-----------------

@pytest.mark.parametrize("field, value", EDGE_CASES_PASSWORD_VALID)
def test_valid_password(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value

    try:
        result = schema.load(cop)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid password '{value}': {excinfo}")

@pytest.mark.parametrize("field, value", EDGE_CASES_PASSWORD)
def test_invalid_password(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value
        
    with pytest.raises(ValidationError) as excinfo:
        schema.load(cop)
        
    assert field in excinfo.value.messages

    #-----------------
    #Status Tests
    #-----------------

@pytest.mark.parametrize("field, value", EDGE_CASES_STATUS_VALID)
def test_valid_status(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value

    try:
        result = schema.load(cop)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid status '{value}': {excinfo}")

@pytest.mark.parametrize("field, value", EDGE_CASES_STATUS)
def test_invalid_status(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value
        
    with pytest.raises(ValidationError) as excinfo:
        schema.load(cop)
        
    assert field in excinfo.value.messages

    #-----------------
    #Latitude Tests
    #-----------------

@pytest.mark.parametrize("field, value", EDGE_CASES_LATITUDE_VALID)
def test_valid_latitude(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value

    try:
        result = schema.load(cop)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid latitude '{value}': {excinfo}")

@pytest.mark.parametrize("field, value", EDGE_CASES_LATITUDE)
def test_invalid_latitude(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value
        
    with pytest.raises(ValidationError) as excinfo:
        schema.load(cop)
        
    assert field in excinfo.value.messages

    #-----------------
    #Longitude Tests
    #-----------------

@pytest.mark.parametrize("field, value", EDGE_CASES_LONGITUDE_VALID)
def test_valid_longitude(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value

    try:
        result = schema.load(cop)
        assert result[field] == value
    except ValidationError as excinfo:
        pytest.fail(f"Unexpected ValidationError for valid longitude '{value}': {excinfo}")

@pytest.mark.parametrize("field, value", EDGE_CASES_LONGITUDE)
def test_invalid_longitude(schema, valid_user_dict,field,value):
    cop = valid_user_dict.copy()
    cop[field] = value
        
    with pytest.raises(ValidationError) as excinfo:
        schema.load(cop)
        
    assert field in excinfo.value.messages






