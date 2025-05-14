# 🎯 FastAPI Parameter Validation Learning

## 📚 Overview
This project demonstrates different types of parameter validation in FastAPI, including path parameters, query parameters, and request bodies.

## 📝 Related Blog Post
Check out my detailed blog post about API Parameters in FastAPI:
[API Parameters in FastAPI: The Ultimate Guide](https://mughalsyntax.hashnode.dev/api-parameters-in-fastapi-the-ultimate-guide)

## 🔍 Features Implemented

### 1. Path Parameters
- Basic path parameter validation
- Numeric constraints (ge, le)
- Required parameters
- Example: `/items/{item_id}`

### 2. Query Parameters
- Optional and required query parameters
- String length validation
- Numeric range validation
- Multiple query parameters
- Example: `/search/?q=phone&skip=0&limit=10`

### 3. Request Body
- Pydantic model validation
- Optional fields
- Type validation
- Example data

### 4. Combined Parameters
- Path + Query + Body parameters
- Complex validation scenarios
- Error handling

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

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

## 📝 API Endpoints

1. **GET /items/{item_id}**
   - Path parameter validation
   - Requires positive integer ID

2. **GET /search/**
   - Multiple query parameters
   - Optional search query (3-50 chars)
   - Pagination support

3. **PUT /items/{item_id}**
   - Combined parameter types
   - Request body validation
   - Optional query parameter

4. **GET /filter/**
   - List parameters
   - Price range filtering
   - Multiple categories

## 💡 Key Learning Points

1. **Parameter Types**
   - Path Parameters (`Path()`)
   - Query Parameters (`Query()`)
   - Request Body (`Body()`)

2. **Validation Features**
   - Numeric constraints (ge, le, gt, lt)
   - String validation (min_length, max_length)
   - Optional vs Required fields
   - Default values

3. **Documentation**
   - Automatic OpenAPI generation
   - Example values
   - Detailed descriptions

4. **Error Handling**
   - HTTP exceptions
   - Validation errors
   - Custom error messages

## 🔍 Testing the API

1. Use the Swagger UI at `/docs`
2. Try invalid inputs to see validation errors
3. Test different parameter combinations
4. Observe automatic type conversion

---
*Created with 💖 by Ayesha Mughal while learning FastAPI parameter validation*
