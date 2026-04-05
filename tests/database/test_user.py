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

#-------------
#Model Method Tests
#-------------

def test_password_hashing(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    user.set_password(valid_user_dict["password"])
    assert user.password_hash != valid_user_dict["password"]  # Ensure password is hashed
    assert user.check_password(valid_user_dict["password"])[0] == True  # Check correct password

def test_check_password_invalid(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    user.set_password(valid_user_dict["password"])
    assert user.check_password("WrongPassword1!")[0] == False  # Check incorrect password

def test_check_password_edge_cases(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    user.set_password(valid_user_dict["password"])
    
    # Test non-string password
    assert user.check_password(12345) == (False, "Password must be a non-empty string.")
    
    # Test too short password
    assert user.check_password("short1!") == (False, "Password must be between 8 and 128 characters long.")

def test_to_dict(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    user.set_password(valid_user_dict["password"])
    user_dict = user.to_dict()

    assert user_dict["id"] == None  # ID should be None before being added to the database
    assert user_dict["badge_num"] == valid_user_dict["badge_num"]
    assert user_dict["name"] == valid_user_dict["name"]
    assert user_dict["latitude"] == valid_user_dict["latitude"]
    assert user_dict["longitude"] == valid_user_dict["longitude"]
    assert user_dict["status"] == valid_user_dict["status"]
    assert "password" not in user_dict

def test_set_admin(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    assert user.admin == False  # Default should be False
    user.set_admin()
    assert user.admin == True   # Should toggle to True
    user.set_admin()
    assert user.admin == False  # Should toggle back to False

def test_update_status(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    assert user.status == valid_user_dict["status"]  # Initial status
    user.status = "Away"
    assert user.status == "Away"  # Updated status

def test_update_status_invalid(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    # Attempt to set an invalid status
    result = user.update_status("Busy")
    assert result == (False, "Status must be one of ['Online', 'Offline', 'Away']")
    assert user.status == valid_user_dict["status"]  # Status should remain unchanged

def test_set_location(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    # Update location with valid coordinates
    result = user.set_location(37.7749, -122.4194)
    assert result == (True, None)
    assert user.latitude == 37.7749
    assert user.longitude == -122.4194

def test_set_location_invalid(valid_user_dict):
    user = User(
        badge_num=valid_user_dict["badge_num"],
        name=valid_user_dict["name"],
        latitude=valid_user_dict["latitude"],
        longitude=valid_user_dict["longitude"],
        status=valid_user_dict["status"]
    )

    # Attempt to set invalid latitude and longitude
    result = user.set_location(-100.0, 200.0)
    assert result == (False, "Latitude must be between -90 and 90.")
    assert user.latitude == valid_user_dict["latitude"]  # Latitude should remain unchanged
    assert user.longitude == valid_user_dict["longitude"]  # Longitude should remain unchanged







