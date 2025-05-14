from pydantic import BaseModel, ValidationError

# Yahan pr main ek basic model bana rahi hun - Simple User Model
# inhesrited from base model to have validation
class User(BaseModel):
    id: int  
    name: str  
    email: str  
    age: int | None = None 

#Now testing with valid data
# all fields proper hain
user_data = {"id": 1, "name": "Ayesha Mughal", "email": "ayeshamughal2162@gmail.com", "age": 15}
user = User(**user_data) #used ** to unpack dic
print("Valid data ka result:")
print(user)  
print(user.model_dump())  # to get data in dictionary form

# Now testing with invalid data
# id is not an integer and added string inplace of integer here
try:
    invalid_user = User(id="not_an_int", name="Emaan Zai", email="eman@example.com")
except ValidationError as e:
    print("\nError agaya bhai:")
    print(e)  # Error message dikhayega
