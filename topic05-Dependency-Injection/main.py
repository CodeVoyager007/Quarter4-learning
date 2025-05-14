from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import Annotated
from pydantic import BaseModel

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Dependency Injection Examples",
    description="""
    Learning Dependency Injection in FastAPI through practical examples.
    
    Features:
    - Simple Dependencies
    - Dependencies with Parameters
    - Query Parameter Dependencies
    - Multiple Dependencies
    - Class-based Dependencies
    
    Created by: Ayesha Mughal
    """,
    version="1.0.0",
    contact={
        "name": "Ayesha Mughal",
        "url": "https://mughalsyntax.hashnode.dev/",
    }
)

# 1. Simple Dependency Example
# Yahan pe simple dependency banai hai jo ek dictionary return karti hai
def get_simple_goal():
    """Simple dependency that returns a goal"""
    return {"goal": "We are building AI Agents Workforce"}
    
@app.get("/get-simple-goal", tags=["Simple Dependencies"])
def simple_goal(response: Annotated[dict, Depends(get_simple_goal)]):
    """Endpoint using simple dependency"""
    return response

# 2. Dependency with Parameter
# Ab hum parameters ke sath dependency use karenge
def get_goal(username: str):
    """Dependency that uses a parameter"""
    return {
        "goal": "We are building AI Agents Workforce",
        "username": username
    }
    
@app.get("/get-goal", tags=["Dependencies with Parameters"])
def get_my_goal(response: Annotated[dict, Depends(get_goal)]):
    """Endpoint using dependency with parameter"""
    return response

# 3.Dependency with Query Parameters
# Query parameters ke sath login dependency
def dep_login(
    username: str = Query(None, description="Admin username"),
    password: str = Query(None, description="Admin password")
):
    """Login dependency using query parameters"""
    if username == "admin" and password == "admin":
        return {"message": "Login Successful", "status": "success"}
    else:
        return {"message": "Login Failed", "status": "failed"}
    
@app.get("/signin", tags=["Query Parameter Dependencies"])
def login_api(user: Annotated[dict, Depends(dep_login)]):
    """Login endpoint using query parameter dependency"""
    return user

# 4. Multiple Dependencies Example # Multiple dependencies ko combine karna
def depfunc1(num: int): 
    """First dependency that adds 1"""
    num = int(num)
    num += 1
    return num
def depfunc2(num: int): 
    """Second dependency that adds 2"""
    num = int(num)
    num += 2
    return num
@app.get("/main/{num}", tags=["Multiple Dependencies"])
def get_main(
    num: int,
    num1: Annotated[int, Depends(depfunc1)],
    num2: Annotated[int, Depends(depfunc2)]
):
    """Endpoint using multiple dependencies"""
    total = num + num1 + num2  
    return f"Total: {total} (Original: {num}, First Dep: {num1}, Second Dep: {num2})"

# 5. Class-based Dependencies
# Database simulation with dictionaries
blogs = {
    "1": "Generative AI Blog",
    "2": "Machine Learning Blog",
    "3": "Deep Learning Blog"
}
users = {
    "8": "Ahmed",
    "9": "Mohammed"
}
# Generic class for handling not found errors
class GetObjectOr404:
    """Class-based dependency for handling 404 errors"""
    def __init__(self, model: dict) -> None:
        self.model = model

    def __call__(self, id: str):
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID {id} not found"
            )
        return obj

# Create dependencies for blogs and users
blog_dependency = GetObjectOr404(blogs)
user_dependency = GetObjectOr404(users)

@app.get("/blog/{id}", tags=["Class Dependencies"])
def get_blog(blog_name: Annotated[str, Depends(blog_dependency)]):
    """Get blog using class-based dependency"""
    return {"blog": blog_name}

@app.get("/user/{id}", tags=["Class Dependencies"])
def get_user(user_name: Annotated[str, Depends(user_dependency)]):
    """Get user using class-based dependency"""
    return {"user": user_name}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint showing available examples"""
    return {
        "message": "Welcome to FastAPI Dependency Injection Examples! 👋",
        "examples": {
            "1. Simple Dependency": "/get-simple-goal",
            "2. Dependency with Parameter": "/get-goal?username=YourName",
            "3. Query Parameter Login": "/signin?username=admin&password=admin",
            "4. Multiple Dependencies": "/main/5",
            "5. Class Dependencies": {
                "Blog": "/blog/1",
                "User": "/user/8"
            }
        },
        "documentation": {
            "Swagger UI": "/docs",
            "ReDoc": "/redoc"
        }
    }
