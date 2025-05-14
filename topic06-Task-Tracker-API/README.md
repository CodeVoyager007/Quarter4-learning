# Enhanced Task Tracker API

A powerful and feature-rich Task Management API built with FastAPI that helps users manage tasks, track progress, and stay organized.

## Features

### Task Management
- ✨ Create and manage tasks with detailed attributes
- 🎯 Set task priorities (Low, Medium, High, Urgent)
- 📊 Track task progress with percentage completion
- 🏷️ Categorize tasks (Work, Study, Personal, Health, Shopping, Other)
- 🔖 Add custom tags to tasks
- ⏰ Set due dates and reminders
- 📈 Track estimated hours

### Task Status Workflow
- 📝 Todo
- 🔄 In Progress
- 👀 Under Review
- ✅ Completed
- 📦 Archived

### User Management
- 👤 User profiles with customizable settings
- 🌐 Timezone support
- 🔔 Configurable notification preferences
- 📧 Email validation
- 🔐 Secure password handling

### Analytics and Insights
- 📊 Task completion statistics
- 📈 Progress tracking
- 📅 Deadline monitoring
- 📊 Category distribution analysis
- 🎯 Priority-based analytics

## Technical Stack

- **Framework**: FastAPI
- **Data Validation**: Pydantic
- **Python Version**: 3.13.2
- **Documentation**: OpenAPI (Swagger) and ReDoc

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd topic06-Task-Tracker-API
```

2. Create and activate a virtual environment:
```bash
# Using uv (recommended)
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
uv pip install fastapi[all] pydantic[email] python-multipart
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- API Endpoint: http://127.0.0.1:8000
- Interactive Docs: http://127.0.0.1:8000/docs
- Alternative Docs: http://127.0.0.1:8000/redoc

## API Endpoints

### User Management

#### Create User
```http
POST /users/
```
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "secretpass123",
  "profile": {
    "bio": "Software Developer",
    "timezone": "UTC",
    "notification_preferences": {
      "email": true,
      "in_app": true,
      "deadline_reminder": true
    }
  }
}
```

#### Get User Details
```http
GET /users/{user_id}
```

### Task Management

#### Create Task
```http
POST /tasks/
```
```json
{
  "title": "Complete Project",
  "description": "Implement new features",
  "due_date": "2024-03-30",
  "priority": "high",
  "category": "work",
  "tags": ["coding", "fastapi"],
  "estimated_hours": 8,
  "user_id": 1
}
```

#### Update Task
```http
PUT /tasks/{task_id}
```

#### Search Tasks
```http
GET /tasks/search/?query=project&category=work&priority=high
```

### Analytics

#### Get User Statistics
```http
GET /users/{user_id}/stats
```

#### Get Upcoming Deadlines
```http
GET /users/{user_id}/deadlines?days=7
```

## Error Handling

The API includes comprehensive error handling:
- 404: Resource not found
- 400: Bad request / validation errors
- 422: Unprocessable entity

## Data Validation

- Username: 3-20 characters
- Email: Valid email format
- Progress: 0-100%
- Due dates: Must be future dates
- Required fields validation
- Custom validators for specific fields

## Best Practices

1. **Task Updates**:
   - Update task status regularly
   - Track progress percentage
   - Add relevant tags

2. **User Management**:
   - Set appropriate timezone
   - Configure notification preferences
   - Keep profile information updated

3. **Task Organization**:
   - Use appropriate categories
   - Set realistic deadlines
   - Update progress regularly

## Author

Created by: Ayesha Mughal
Blog: https://mughalsyntax.hashnode.dev/

## Version

Current Version: 1.0.0

## License

[Add your license information here]
