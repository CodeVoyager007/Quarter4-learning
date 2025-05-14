from pydantic import BaseModel, EmailStr, validator, ValidationError
from typing import List

# Address model old one
class Address(BaseModel):
    street: str  
    city: str   
    zip_code: str  

# Adding Custom validation
class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    addresses: List[Address]

    # Custom validator function 
    # Using decorator to validate
    @validator("name")
    def name_must_be_at_least_two_chars(cls, v):
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")  
        return v

# testin with invalid data
print("Invalid data test...")
try:
    invalid_user = UserWithAddress(
        id=3,
        name="A",  
        email="maano@example.com",
        addresses=[{"street": "789 Pine Rd", "city": "Chicago", "zip_code": "60601"}],
    )
except ValidationError as e:
    print("\nError will be shown here:")
    print(e)