from fastapi import FastAPI, Path, Query, Body, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app 
app = FastAPI(
    title="Parameter Validation API",
    description="""
    A learning project demonstrating different types of API parameters in FastAPI.
    
    Features:
    - Path Parameters
    - Query Parameters
    - Request Body Validation
    - Combined Parameters
    - Error Handling
    
    Created by: Ayesha Mughal
    """,
    version="1.0.0",
    contact={
        "name": "Ayesha Mughal",
        "url": "https://mughalsyntax.hashnode.dev/",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint that provides API information and available endpoints.
    """
    return {
        "message": "Welcome to the Parameter Validation API! 👋",
        "description": "This API demonstrates different types of parameter validation in FastAPI",
        "available_endpoints": {
            "documentation": {
                "Swagger UI": "/docs",
                "ReDoc": "/redoc",
            },
            "endpoints": {
                "items": "/items/{item_id}",
                "search": "/search/",
                "update": "/items/{item_id}",
                "filter": "/filter/",
                "validate": "/items/{item_id}/validate"
            }
        },
        "author": "Ayesha Mughal",
        "version": "1.0.0"
    }

# Pydantic model for our Item
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: bool = False

# 1.Path parameter example with Validation
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ...,  # ... means required
        title="The ID of the item",
        description="A unique identifier for the item in our database",
        ge=1,  # must be greater than or equal to 1
        example=123
    )
):
    """
    Get an item by its ID.
    - **item_id**: Must be a positive integer
    """
    return {
        "item_id": item_id,
        "message": f"You requested item #{item_id}"
    }

# 2. Query parameters example with Validation
@app.get("/search/")
async def search_items(
    q: str | None = Query(
        None,  # Default value is None (optional parameter)
        title="Search Query",
        description="Search items by name or description",
        min_length=3,
        max_length=50,
        example="phone"
    ),
    category: str | None = Query(
        None,
        title="Category Filter",
        description="Filter items by category"
    ),
    skip: int = Query(
        0, 
        ge=0,  # Greater than or equal to 0
        title="Skip Records",
        description="Number of records to skip for pagination"
    ),
    limit: int = Query(
        10, 
        le=100,  # Less than or equal to 100
        title="Limit Records",
        description="Maximum number of records to return"
    )
):
    """
    Search for items with various filters:
    - **q**: Optional search query (3-50 characters)
    - **category**: Optional category filter
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    return {
        "search_query": q,
        "category": category,
        "skip": skip,
        "limit": limit
    }
# 3.Combined parameters (Path + Query + Body)
@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(
        ..., 
        title="Item ID",
        description="The ID of the item to update",
        ge=1
    ),
    q: str | None = Query(
        None,
        title="Query String",
        description="Additional query parameter",
        min_length=3
    ),
    item: Item = Body(
        ...,
        title="Item Data",
        description="The item data to update",
        example={
            "name": "Smartphone",
            "description": "Latest model",
            "price": 999.99,
            "is_offer": True
        }
    )
):
    """
    Update an item with combined parameters:
    - **item_id**: Path parameter for item identification
    - **q**: Optional query parameter
    - **item**: Request body containing item data
    """
    result = {
        "item_id": item_id,
        "item_data": item.model_dump()
    }
    if q:
        result["query"] = q
    return result
# 4.Multiple query parameters with List
@app.get("/filter/")
async def filter_items(
    categories: list[str] = Query(
        None,
        title="Categories",
        description="Filter by multiple categories",
        example=["electronics", "phones"]
    ),
    price_range: tuple[float, float] | None = Query(
        None,
        title="Price Range",
        description="Filter by price range (min, max)",
        example=[0, 1000]
    )
):
    """
    Filter items by multiple parameters:
    - **categories**: List of categories to filter by
    - **price_range**: Tuple of (min_price, max_price)
    """
    return {
        "categories": categories,
        "price_range": price_range
    }

# Error handling example
@app.get("/items/{item_id}/validate")
async def validate_item(
    item_id: int = Path(..., ge=1),
    strict: bool = Query(False, title="Strict Mode")
):
    """
    Example of error handling with parameters:
    - **item_id**: Must be positive
    - **strict**: Enable strict validation
    """
    if strict and item_id > 100:
        raise HTTPException(
            status_code=400,
            detail="Item ID cannot be greater than 100 in strict mode"
        )
    return {"item_id": item_id, "strict_mode": strict} 