from pydantic import BaseModel, EmailStr

# Nested model concept 
# 1st will create address model then we will use   it in user model

# Address ke liye separate sub model 
class Address(BaseModel):
    street: str  
    city: str   
    zip_code: str  

# Main User model with nested Address it is complex model
class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr  
    addresses: list[Address]  

# Test data--Proper nested structure 
user_data = {
    "id": 2,
    "name": "Maryam Khan",
    "email": "maryam@example.com",
    "addresses": [
        {"street": "Urdu Bazar", "city": "Karachi", "zip_code": "10001"}, 
        {"street": "Fort Road", "city": "Lahore", "zip_code": "90001"},  
    ],
}

# create object to validate data
user = UserWithAddress.model_validate(user_data)
print("Nested data's output is:")
print(user.model_dump()) 