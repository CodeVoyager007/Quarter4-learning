from fastapi import FastAPI, HTTPException, Path, Query, Depends
from pydantic import BaseModel, EmailStr, constr, validator, Field
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from enum import Enum
from collections import defaultdict

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Enhanced Task Tracker API",
    description="""
    An Advanced Task Management API that allows users to:
    - Create and manage users with profiles
    - Create and track tasks with priorities and categories
    - Update task status and progress
    - Get task statistics and analytics
    - Search and filter tasks
    - Set task reminders and deadlines
    
    Created by: Ayesha Mughal
    """,
    version="1.0.0",
    contact={
        "name": "Ayesha Mughal",
        "url": "https://mughalsyntax.hashnode.dev/",
    }
)

# Enhanced Enums
class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    UNDER_REVIEW = "under_review"  
    COMPLETED = "completed"
    ARCHIVED = "archived"  

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskCategory(str, Enum):
    WORK = "work"
    STUDY = "study"
    PERSONAL = "personal"
    HEALTH = "health"
    SHOPPING = "shopping"
    OTHER = "other"

# Enhanced Pydantic Models
class UserBase(BaseModel):
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    full_name: str

class UserProfile(BaseModel):
    bio: Optional[str] = None
    timezone: str = "UTC"
    notification_preferences: Dict[str, bool] = {
        "email": True,
        "in_app": True,
        "deadline_reminder": True
    }

class UserCreate(UserBase):
    password: str
    profile: Optional[UserProfile] = None

class UserRead(UserBase):
    id: int
    created_at: datetime
    profile: Optional[UserProfile] = None
    task_count: int = 0

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    category: TaskCategory = TaskCategory.OTHER
    tags: List[str] = Field(default_factory=list)
    estimated_hours: Optional[float] = None
    progress_percentage: int = Field(0, ge=0, le=100)

    @validator('due_date')
    def ensure_future_date(cls, v):
        if v < date.today():
            raise ValueError("Due date must be today or in the future")
        return v

    @validator('progress_percentage')
    def update_status_based_on_progress(cls, v, values):
        if v == 100 and values.get('status') != TaskStatus.COMPLETED:
            values['status'] = TaskStatus.COMPLETED
        return v

class TaskCreate(TaskBase):
    user_id: int

class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    reminder_date: Optional[datetime] = None

# Simulated database
users_db = {}
tasks_db = {}
user_id_counter = 1
task_id_counter = 1

# Helper Functions
def get_upcoming_deadlines(user_id: int, days: int = 7) -> List[Task]:
    """Get tasks with deadlines in the next X days"""
    future_date = date.today() + timedelta(days=days)
    return [
        task for task in tasks_db.values()
        if task["user_id"] == user_id 
        and task["due_date"] <= future_date
        and task["status"] != TaskStatus.COMPLETED
    ]

def calculate_user_stats(user_id: int) -> dict:
    """Calculate task statistics for a user"""
    user_tasks = [task for task in tasks_db.values() if task["user_id"] == user_id]
    stats = {
        "total_tasks": len(user_tasks),
        "completed_tasks": len([t for t in user_tasks if t["status"] == TaskStatus.COMPLETED]),
        "urgent_tasks": len([t for t in user_tasks if t["priority"] == TaskPriority.URGENT]),
        "overdue_tasks": len([t for t in user_tasks if t["due_date"] < date.today() and t["status"] != TaskStatus.COMPLETED]),
        "tasks_by_category": defaultdict(int),
        "average_progress": 0
    }
    
    if user_tasks:
        stats["average_progress"] = sum(t["progress_percentage"] for t in user_tasks) / len(user_tasks)
        for task in user_tasks:
            stats["tasks_by_category"][task["category"]] += 1
    
    return stats

# Enhanced User endpoints
@app.post("/users/", response_model=UserRead, tags=["Users"])
async def create_user(user: UserCreate):
    """Create a new user with profile"""
    global user_id_counter
    user_dict = user.model_dump()
    user_dict["id"] = user_id_counter
    user_dict["created_at"] = datetime.now()
    user_dict["task_count"] = 0
    users_db[user_id_counter] = user_dict
    user_id_counter += 1
    return user_dict

@app.get("/users/{user_id}", response_model=UserRead, tags=["Users"])
async def get_user(user_id: int = Path(..., description="The ID of the user to retrieve")):
    """Get user details and profile"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user = users_db[user_id]
    user["task_count"] = len([t for t in tasks_db.values() if t["user_id"] == user_id])
    return user

# Enhanced Task endpoints
@app.post("/tasks/", response_model=Task, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """Create a new task with enhanced features"""
    global task_id_counter
    if task.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    task_dict = task.model_dump()
    task_dict["id"] = task_id_counter
    task_dict["created_at"] = datetime.now()
    task_dict["updated_at"] = datetime.now()
    
    # Set reminder date (1 day before due date)
    task_dict["reminder_date"] = datetime.combine(
        task.due_date - timedelta(days=1),
        datetime.min.time()
    )
    
    tasks_db[task_id_counter] = task_dict
    task_id_counter += 1
    return task_dict

@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(
    task_id: int = Path(..., description="The ID of the task to update"),
    status: Optional[TaskStatus] = Query(None, description="New status"),
    progress: Optional[int] = Query(None, ge=0, le=100, description="Progress percentage"),
    priority: Optional[TaskPriority] = Query(None, description="Task priority")
):
    """Update task status, progress, and priority"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    if status:
        task["status"] = status
    if progress is not None:
        task["progress_percentage"] = progress
        if progress == 100:
            task["status"] = TaskStatus.COMPLETED
    if priority:
        task["priority"] = priority
    
    task["updated_at"] = datetime.now()
    return task

# New Enhanced Endpoints
@app.get("/users/{user_id}/stats", tags=["Analytics"])
async def get_user_stats(user_id: int):
    """Get detailed task statistics for a user"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return calculate_user_stats(user_id)

@app.get("/users/{user_id}/deadlines", response_model=List[Task], tags=["Tasks"])
async def get_upcoming_tasks(
    user_id: int,
    days: int = Query(7, ge=1, le=30, description="Number of days to look ahead")
):
    """Get upcoming task deadlines"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return get_upcoming_deadlines(user_id, days)

@app.get("/tasks/search/", response_model=List[Task], tags=["Tasks"])
async def search_tasks(
    user_id: int,
    query: Optional[str] = None,
    category: Optional[TaskCategory] = None,
    priority: Optional[TaskPriority] = None,
    status: Optional[TaskStatus] = None,
    tag: Optional[str] = None
):
    """Search tasks with multiple filters"""
    tasks = [t for t in tasks_db.values() if t["user_id"] == user_id]
    
    if query:
        tasks = [t for t in tasks if query.lower() in t["title"].lower() or 
                (t["description"] and query.lower() in t["description"].lower())]
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if tag:
        tasks = [t for t in tasks if tag in t["tags"]]
    
    return tasks

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint with enhanced API information"""
    return {
        "message": "Welcome to the Enhanced Task Tracker API! 📝",
        "features": {
            "Task Management": [
                "Priority levels",
                "Categories",
                "Progress tracking",
                "Tags",
                "Reminders",
                "Status workflow"
            ],
            "Analytics": [
                "Task statistics",
                "Deadline tracking",
                "Category distribution"
            ],
            "User Features": [
                "User profiles",
                "Notification preferences",
                "Timezone support"
            ]
        },
        "endpoints": {
            "users": {
                "create_user": "POST /users/",
                "get_user": "GET /users/{user_id}",
                "get_stats": "GET /users/{user_id}/stats"
            },
            "tasks": {
                "create_task": "POST /tasks/",
                "update_task": "PUT /tasks/{task_id}",
                "search_tasks": "GET /tasks/search/",
                "upcoming_deadlines": "GET /users/{user_id}/deadlines"
            }
        },
        "documentation": {
            "Swagger UI": "/docs",
            "ReDoc": "/redoc"
        }
    }
