# 🔄 FastAPI Dependency Injection Learning

## 📚 Overview
This project demonstrates different ways to use Dependency Injection in FastAPI, making code more reusable and maintainable.

## 📝 Related Blog Post
Check out my detailed blog post about Dependency Injection in FastAPI:
[Dependency Injection in FastAPI: Cleaner, Smarter APIs](https://mughalsyntax.hashnode.dev/dependency-injection-in-fastapi-cleaner-smarter-apis)

## 🌟 Features Implemented

### 1. Simple Dependencies
```python
def get_simple_goal():
    return {"goal": "We are building AI Agents Workforce"}
    
@app.get("/get-simple-goal")
def simple_goal(response: Annotated[dict, Depends(get_simple_goal)]):
    return response
```

### 2. Dependencies with Parameters
```python
def get_goal(username: str):
    return {"goal": "Goal", "username": username}
```

### 3. Query Parameter Dependencies
```python
def dep_login(username: str, password: str):
    if username == "admin" and password == "admin":
        return {"message": "Login Successful"}
```

### 4. Multiple Dependencies
```python
@app.get("/main/{num}")
def get_main(
    num: int,
    num1: Annotated[int, Depends(depfunc1)],
    num2: Annotated[int, Depends(depfunc2)]
)
```

### 5. Class-based Dependencies
```python
class GetObjectOr404:
    def __init__(self, model: dict) -> None:
        self.model = model

    def __call__(self, id: str):
        # Handle 404 errors
```

## 🚀 Running the Application

1. **Setup Virtual Environment**
   ```bash
   uv venv
   .venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   uv add "fastapi[standard]"
   ```

3. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

## 📝 API Endpoints

1. **GET /**
   - Welcome page with examples

2. **GET /get-simple-goal**
   - Simple dependency example

3. **GET /get-goal**
   - Dependency with parameter
   - Query param: `username`

4. **GET /signin**
   - Login with query parameters
   - Query params: `username`, `password`

5. **GET /main/{num}**
   - Multiple dependencies example
   - Path param: `num`

6. **GET /blog/{id}**
   - Class-based dependency example
   - Path param: `id`

7. **GET /user/{id}**
   - Class-based dependency example
   - Path param: `id`

## 💡 Key Learning Points

1. **Types of Dependencies**
   - Function-based dependencies
   - Class-based dependencies
   - Query parameter dependencies
   - Multiple dependencies

2. **Dependency Features**
   - Parameter validation
   - Error handling
   - Reusable code
   - Clean architecture

3. **Best Practices**
   - Use dependencies for reusable logic
   - Handle errors gracefully
   - Document dependencies
   - Use type hints

## 🔍 Testing the API

1. Simple Goal:
   ```
   GET /get-simple-goal
   ```

2. Login (Success):
   ```
   GET /signin?username=admin&password=admin
   ```

3. Blog (Success):
   ```
   GET /blog/1
   ```

4. Blog (404 Error):
   ```
   GET /blog/999
   ```

## 📈 Next Steps

1. Add more complex dependencies
2. Implement database connections
3. Add authentication dependencies
4. Create nested dependencies

---
*Created with 💖 by Ayesha Mughal while learning FastAPI Dependency Injection*

