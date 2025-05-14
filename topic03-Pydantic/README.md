# 🚀 Learning Pydantic: Data Validation 

## 📚 Overview
This project demonstrates my journey learning Pydantic, a powerful data validation library for Python. Through practical examples, I've explored how Pydantic makes data handling safer and more efficient.

## 📝 Related Blog Post
Check out my detailed blog post about Pydantic:
[Pydantic: The Elegant Guardian of Python Data](https://mughalsyntax.hashnode.dev/pydantic-the-elegant-guardian-of-python-data)

## 🌟 Key Concepts Learned

### 1. Basic Model Definition
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None  # Optional field
```
> **Learning**: Models are like blueprints that ensure data consistency and type safety.

### 2. 🏗️ Nested Models
```python
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserWithAddress(BaseModel):
    name: str
    addresses: list[Address]
```
> **Learning**: Complex data structures can be validated hierarchically.

### 3. ✨ Data Validation Features
- **Type Validation**: Automatic type checking and conversion
- **Custom Validators**: Define specific validation rules
- **Error Handling**: Detailed error messages for invalid data
- **Default Values**: Flexible field definitions
- **Serialization**: Easy conversion to/from JSON

### 4. 🛠️ Practical Applications

#### FastAPI Integration
```python
@app.post("/chat/", response_model=Response)
async def chat(message: Message):
    if not message.text.strip():
        raise HTTPException(status_code=400)
    return Response(...)
```

## 🔍 Examples in This Project

1. **Basic Model** (`pydantic_example_1.py`)
   - Simple user model
   - Basic validation
   - Error handling

2. **Nested Models** (`pydantic_example_2.py`)
   - Address and user relationship
   - Complex data structures
   - List field validation

3. **Custom Validation** (`pydantic_example_3.py`)
   - Custom validator decorators
   - Specific validation rules
   - Advanced error handling

4. **FastAPI Integration** (`main.py`)
   - Real-world API implementation
   - Request/Response models
   - Complete validation pipeline

## 🚀 Running the Examples

1. **Setup Virtual Environment**
   ```bash
   uv venv
   .venv/Scripts/activate
   ```

2. **Install Dependencies**
   ```bash
   uv pip install "fastapi[all]" pydantic email-validator
   ```

3. **Run Examples**
   ```bash
   # Basic examples
   python pydantic_example_1.py
   python pydantic_example_2.py
   python pydantic_example_3.py

   # FastAPI application
   uvicorn main:app --reload
   ```

## 💡 Key Takeaways

1. **Type Safety**: Pydantic ensures data integrity through strong typing
2. **Validation**: Automatic validation saves time and reduces errors
3. **Integration**: Seamless integration with FastAPI for building robust APIs
4. **Flexibility**: Support for complex data structures and custom validation
5. **Developer Experience**: Excellent error messages and documentation

## 🌟 What I've Learned

- How to create type-safe data models
- Implementing nested data structures
- Writing custom validators
- Integrating Pydantic with FastAPI
- Handling complex data validation scenarios
- Best practices for API development

---
*Created with 💖 by Ayesha Mughal while learning Python data validation*
