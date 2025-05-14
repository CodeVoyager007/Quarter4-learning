from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from uuid import uuid4

#INitializing FastAPI 
# For Documentation setting title, description and version
app = FastAPI(
    title="DACA Chatbot API",
    description="A FastAPI-based API for a chatbot in the DACA tutorial series",
    version="0.1.0",
)

# Complex Pydantic models 
class Metadata(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))  # Auto timestamp
    session_id: str = Field(default_factory=lambda: str(uuid4()))  # Unique session ID

# Message mode
class Message(BaseModel):
    user_id: str  
    text: str    
    metadata: Metadata  
    tags: list[str] | None = None 
    
# Response model - returning response 
class Response(BaseModel):
    user_id: str  
    reply: str   
    metadata: Metadata  

# Root endpoint - Basic welcome message
@app.get("/")
async def root():
    return {"message": "Welcome to the DACA Chatbot API! Access /docs for the API documentation."}

# User info endpoint - User ki details get karne ke liye
@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

# Chat endpoint  Main functionality 
@app.post("/chat/", response_model=Response)
async def chat(message: Message):
    # Empty message check 
    if not message.text.strip():
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")
    
    # Simple reply 
    reply_text = f"Hello, {message.user_id}! You said: '{message.text}'. How can I assist you today?"
    
    # response will return in object format
    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()  
    )
