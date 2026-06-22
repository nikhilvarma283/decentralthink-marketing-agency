# Sprint 1-2 Detailed Development Specifications
**Week 1-2: Shared Foundation (54 Story Points)**

All endpoints prefixed with `/api/v1/`

---

## Story 1.1: User Authentication — Sign Up

### Endpoint: `POST /auth/signup`

**Request Body:**
```json
{
  "email": "dentist@practice.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "full_name": "Dr. Smith",
  "role": "dentist"  // or "high_schooler"
}
```

**Validation Rules:**
- Email: Valid format, unique in DB, case-insensitive
- Password: Min 8 chars, 1 uppercase, 1 number, 1 special char
- password_confirm: Must match password
- full_name: Non-empty, max 100 chars
- role: Must be "dentist" or "high_schooler"

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "dentist@practice.com",
    "full_name": "Dr. Smith",
    "role": "dentist",
    "created_date": "2026-06-22T10:30:00Z"
  },
  "message": "User created successfully"
}
```

**Response (400 - Validation Error):**
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Email already exists"
}
```

**Response (400 - Password Mismatch):**
```json
{
  "success": false,
  "error": "validation_error",
  "message": "Passwords do not match"
}
```

**Backend Implementation:**
```python
# app/routes/auth.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import SignUpRequest, UserResponse
from app.services.auth_service import signup_user
from app.database import get_db

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    return await signup_user(db, request)
```

```python
# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, field_validator
import re

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str
    full_name: str
    role: str  # dentist or high_schooler
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain number')
        if not re.search(r'[!@#$%^&*]', v):
            raise ValueError('Password must contain special char')
        return v
    
    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_date: datetime
```

```python
# app/services/auth_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User, UserRole
from app.utils.password import hash_password
from app.schemas.auth import SignUpRequest

async def signup_user(db: Session, request: SignUpRequest):
    # Check if email exists (case-insensitive)
    existing = db.query(User).filter(
        func.lower(User.email) == request.email.lower()
    ).first()
    
    if existing:
        raise ValueError("Email already exists")
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user
    user = User(
        email=request.email.lower(),
        password_hash=password_hash,
        full_name=request.full_name,
        role=UserRole(request.role)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
```

---

## Story 1.2: User Authentication — Log In & Session Management

### Endpoint: `POST /auth/login`

**Request Body:**
```json
{
  "email": "dentist@practice.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "dentist@practice.com",
      "full_name": "Dr. Smith",
      "role": "dentist"
    }
  }
}
```

**Response (401):**
```json
{
  "success": false,
  "error": "invalid_credentials",
  "message": "Invalid email or password"
}
```

**Backend Implementation:**
```python
# app/routes/auth.py
from datetime import timedelta
from app.config import get_settings
from app.utils.jwt import create_access_token

@router.post("/login")
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        func.lower(User.email) == request.email.lower()
    ).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    settings = get_settings()
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=timedelta(days=30)
    )
    
    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role
            }
        }
    }
```

```python
# app/utils/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import get_settings

def create_access_token(data: dict, expires_delta: timedelta = None):
    settings = get_settings()
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt

def verify_token(token: str):
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None
```

**Frontend Implementation (React):**
```typescript
// frontend/src/services/auth.ts
import api from './api'

export const authService = {
  signup: async (email: string, password: string, full_name: string, role: string) => {
    const response = await api.post('/auth/signup', {
      email,
      password,
      password_confirm: password,
      full_name,
      role
    })
    return response.data
  },
  
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password })
    if (response.data.data.access_token) {
      localStorage.setItem('auth_token', response.data.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.data.user))
    }
    return response.data
  },
  
  logout: () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  }
}
```

---

## Story 1.3: User Profile Management

### Endpoint: `GET /users/profile`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "dentist@practice.com",
    "full_name": "Dr. Smith",
    "role": "dentist",
    "created_date": "2026-06-22T10:30:00Z"
  }
}
```

### Endpoint: `PATCH /users/profile`

**Request Body:**
```json
{
  "full_name": "Dr. James Smith",
  "email": "newemail@practice.com",
  "current_password": "SecurePass123!",
  "new_password": "NewSecurePass456!",
  "new_password_confirm": "NewSecurePass456!"
}
```

All fields optional. `current_password` required if changing email or password.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "newemail@practice.com",
    "full_name": "Dr. James Smith",
    "updated_date": "2026-06-22T11:00:00Z"
  }
}
```

**Backend Implementation:**
```python
# app/routes/users.py
from fastapi import APIRouter, Depends
from app.utils.jwt import verify_token

async def get_current_user(
    token: str = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "created_date": current_user.created_date
        }
    }

@router.patch("/profile")
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify current password if changing email or password
    if request.new_password or request.email:
        if not request.current_password:
            raise HTTPException(status_code=400, detail="Current password required")
        if not verify_password(request.current_password, current_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")
    
    # Update fields
    if request.full_name:
        current_user.full_name = request.full_name
    if request.email:
        current_user.email = request.email.lower()
    if request.new_password:
        current_user.password_hash = hash_password(request.new_password)
    
    db.commit()
    db.refresh(current_user)
    
    return {"success": True, "data": current_user}
```

---

## Story 1.4: Chat Interface — Multi-turn Messaging

### Endpoint: `POST /chat/message`

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440001",
  "content": "What are the best ways to get new patients?"
}
```

**Response (200 - Streaming):**
```
event: start
data: {"session_id": "550e8400...", "message_id": "550e8400..."}

event: token
data: "Patient"

event: token
data: " acquisition"

event: token
data: " is crucial..."

event: end
data: {"total_tokens": 145}
```

**Backend Implementation:**
```python
# app/routes/chat.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import json
import httpx
from app.services.llm_service import stream_claude_response

@router.post("/message")
async def send_message(
    request: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save user message
    user_message = ChatMessage(
        user_id=current_user.id,
        session_id=request.session_id,
        sender="user",
        content=request.content
    )
    db.add(user_message)
    db.commit()
    
    # Get context from prior messages in this session
    prior_messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == request.session_id,
        ChatMessage.id != user_message.id
    ).order_by(ChatMessage.created_date).all()
    
    # Build conversation for Claude
    messages = []
    for msg in prior_messages:
        messages.append({
            "role": "user" if msg.sender == "user" else "assistant",
            "content": msg.content
        })
    messages.append({"role": "user", "content": request.content})
    
    # Stream response from Claude
    async def generate():
        yield f'event: start\ndata: {json.dumps({"session_id": str(request.session_id), "message_id": ""})}\n\n'
        
        full_response = ""
        async for token in stream_claude_response(messages):
            full_response += token
            yield f'event: token\ndata: "{token}"\n\n'
        
        # Save AI response
        ai_message = ChatMessage(
            user_id=current_user.id,
            session_id=request.session_id,
            sender="ai",
            content=full_response,
            tokens_used=len(full_response.split())  # Simple estimate
        )
        db.add(ai_message)
        db.commit()
        
        yield f'event: end\ndata: {json.dumps({"total_tokens": len(full_response.split())})}\n\n'
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

```python
# app/services/llm_service.py
from anthropic import Anthropic
from app.config import get_settings

client = Anthropic()

async def stream_claude_response(messages: list):
    settings = get_settings()
    
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system="You are a helpful marketing assistant for professionals.",
        messages=messages,
        api_key=settings.claude_api_key
    ) as stream:
        for text in stream.text_stream:
            yield text
```

**Frontend Implementation:**
```typescript
// frontend/src/services/chat.ts
export const chatService = {
  sendMessage: async (sessionId: string, content: string, onToken: (token: string) => void) => {
    const response = await fetch('/api/v1/chat/message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
      },
      body: JSON.stringify({ session_id: sessionId, content })
    })
    
    const reader = response.body?.getReader()
    const decoder = new TextDecoder()
    
    while (true) {
      const { done, value } = await reader!.read()
      if (done) break
      
      const text = decoder.decode(value)
      const lines = text.split('\n')
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6)
          if (data.startsWith('"') && data.endsWith('"')) {
            onToken(JSON.parse(data))
          }
        }
      }
    }
  }
}
```

---

## Story 1.5: File Upload in Chat

### Endpoint: `POST /chat/upload`

**Request Body (multipart/form-data):**
```
file: <binary file content>
session_id: 550e8400-e29b-41d4-a716-446655440001
message_id: 550e8400-e29b-41d4-a716-446655440002
```

**Accepted Types:** PDF, DOCX, PNG, JPG  
**Max Size:** 10MB

**Response (200):**
```json
{
  "success": true,
  "data": {
    "file_id": "550e8400-e29b-41d4-a716-446655440003",
    "file_name": "marketing_plan.pdf",
    "file_type": "application/pdf",
    "extracted_text": "Marketing Plan for XYZ Dental...",
    "storage_path": "/uploads/2026-06/marketing_plan.pdf"
  }
}
```

**Backend Implementation:**
```python
# app/routes/chat.py
from fastapi import UploadFile, File
import PyPDF2
from docx import Document
import os

ALLOWED_TYPES = {'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/png', 'image/jpeg'}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

async def extract_text_from_file(file: UploadFile) -> str:
    if file.content_type == 'application/pdf':
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        doc = Document(file.file)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        return "[Image file - OCR not implemented in Phase 1]"

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_id: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    if file.size > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Extract text
    extracted_text = await extract_text_from_file(file)
    
    # Save to storage
    upload_dir = f"uploads/{datetime.now().strftime('%Y-%m')}"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Save to DB
    uploaded_file = UploadedFile(
        user_id=current_user.id,
        message_id=None,  # Can be linked later
        file_name=file.filename,
        file_type=file.content_type,
        file_size=file.size,
        extracted_text=extracted_text[:5000],  # Store first 5000 chars
        storage_path=file_path
    )
    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)
    
    return {
        "success": True,
        "data": {
            "file_id": str(uploaded_file.id),
            "file_name": uploaded_file.file_name,
            "file_type": uploaded_file.file_type,
            "extracted_text": uploaded_file.extracted_text,
            "storage_path": uploaded_file.storage_path
        }
    }
```

---

## Story 1.6: Strategy/Plan Storage

### Endpoint: `POST /strategy/create`

**Request Body:**
```json
{
  "title": "90-Day Marketing Plan",
  "content": "# Marketing Strategy\n\n## Goals...",
  "practice_id": "550e8400-e29b-41d4-a716-446655440000",
  "student_id": null
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "title": "90-Day Marketing Plan",
    "content": "...",
    "status": "draft",
    "created_date": "2026-06-22T12:00:00Z"
  }
}
```

### Endpoint: `GET /strategy/{id}`

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "title": "90-Day Marketing Plan",
    "content": "...",
    "status": "draft",
    "version": "1",
    "created_date": "2026-06-22T12:00:00Z",
    "updated_date": "2026-06-22T12:00:00Z"
  }
}
```

### Endpoint: `PATCH /strategy/{id}`

**Request Body:**
```json
{
  "content": "# Updated Marketing Strategy..."
}
```

**Response (200):** Same as GET

### Endpoint: `POST /strategy/{id}/approve`

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "status": "approved"
  }
}
```

**Backend Implementation:**
```python
# app/routes/strategy.py
from app.models.plan import Plan

@router.post("/create", response_model=PlanResponse)
async def create_strategy(
    request: CreatePlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = Plan(
        user_id=current_user.id,
        practice_id=request.practice_id,
        student_id=request.student_id,
        title=request.title,
        content=request.content,
        status="draft"
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan

@router.get("/{plan_id}", response_model=PlanResponse)
async def get_strategy(
    plan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.patch("/{plan_id}", response_model=PlanResponse)
async def update_strategy(
    plan_id: str,
    request: UpdatePlanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(status_code=404)
    
    plan.content = request.content
    plan.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(plan)
    return plan

@router.post("/{plan_id}/approve")
async def approve_strategy(
    plan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(Plan).filter(
        Plan.id == plan_id,
        Plan.user_id == current_user.id
    ).first()
    if not plan:
        raise HTTPException(status_code=404)
    
    plan.status = "approved"
    db.commit()
    return {"success": True, "data": {"id": str(plan.id), "status": "approved"}}
```

---

## Story 1.7: Stripe Customer Setup

### Backend Implementation

```python
# app/services/stripe_service.py
import stripe
from app.config import get_settings

settings = get_settings()
stripe.api_key = settings.stripe_secret_key

def create_stripe_customer(user: User):
    try:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
            metadata={"user_id": str(user.id)}
        )
        return customer.id
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        return None

# Called after user signup
@router.post("/signup")
async def signup(request: SignUpRequest, db: Session = Depends(get_db)):
    user = User(...)
    db.add(user)
    db.flush()
    
    # Create Stripe customer
    stripe_customer_id = create_stripe_customer(user)
    user.stripe_customer_id = stripe_customer_id
    
    db.commit()
    return user
```

---

## Story 1.9: Basic Analytics Dashboard

### Endpoint: `GET /analytics/summary`

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_users": 45,
    "active_users_7d": 32,
    "active_users_30d": 42,
    "signups_this_week": 12,
    "total_messages": 1234,
    "avg_messages_per_user": 27.4,
    "dentists": 3,
    "high_schoolers": 42,
    "messages_last_7d": 234
  }
}
```

**Backend Implementation:**
```python
# app/routes/analytics.py
from sqlalchemy import func, and_
from datetime import datetime, timedelta

@router.get("/summary")
async def analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Query metrics
    total_users = db.query(func.count(User.id)).scalar()
    active_7d = db.query(func.count(User.id)).filter(
        User.updated_date >= week_ago
    ).scalar()
    active_30d = db.query(func.count(User.id)).filter(
        User.updated_date >= month_ago
    ).scalar()
    
    dentists = db.query(func.count(User.id)).filter(
        User.role == "dentist"
    ).scalar()
    high_schoolers = db.query(func.count(User.id)).filter(
        User.role == "high_schooler"
    ).scalar()
    
    total_messages = db.query(func.count(ChatMessage.id)).scalar()
    messages_7d = db.query(func.count(ChatMessage.id)).filter(
        ChatMessage.created_date >= week_ago
    ).scalar()
    
    avg_messages = total_messages / total_users if total_users > 0 else 0
    
    signups_this_week = db.query(func.count(User.id)).filter(
        User.created_date >= week_ago
    ).scalar()
    
    return {
        "success": True,
        "data": {
            "total_users": total_users,
            "active_users_7d": active_7d,
            "active_users_30d": active_30d,
            "signups_this_week": signups_this_week,
            "total_messages": total_messages,
            "avg_messages_per_user": round(avg_messages, 1),
            "dentists": dentists,
            "high_schoolers": high_schoolers,
            "messages_last_7d": messages_7d
        }
    }
```

---

## Frontend Components (React)

### Login Page
```typescript
// frontend/src/pages/LoginPage.tsx
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../services/auth'

export const LoginPage = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await authService.login(email, password)
      navigate('/dashboard')
    } catch (err) {
      setError('Invalid credentials')
    }
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-900">Login</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && <div className="bg-red-100 text-red-700 p-3 rounded">{error}</div>}
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            />
          </div>
          
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
          >
            Login
          </button>
        </form>
        
        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account? <a href="/signup" className="text-blue-600">Sign up</a>
        </p>
      </div>
    </div>
  )
}
```

### Chat Page
```typescript
// frontend/src/pages/ChatPage.tsx
import { useState, useRef, useEffect } from 'react'
import { chatService } from '../services/chat'
import { v4 as uuidv4 } from 'uuid'

export const ChatPage = () => {
  const [messages, setMessages] = useState<Array<{role: string, content: string}>>([])
  const [input, setInput] = useState('')
  const [sessionId] = useState(uuidv4())
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  
  const handleSend = async () => {
    if (!input.trim()) return
    
    setMessages([...messages, { role: 'user', content: input }])
    setInput('')
    setLoading(true)
    
    let response = ''
    
    try {
      await chatService.sendMessage(sessionId, input, (token) => {
        response += token
      })
      
      setMessages(prev => [...prev, { role: 'assistant', content: response }])
    } catch (err) {
      console.error('Chat error:', err)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="flex flex-col h-screen bg-white">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-md p-3 rounded-lg ${
              msg.role === 'user' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-900'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && <div className="text-gray-500">Thinking...</div>}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="border-t p-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type a message..."
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  )
}
```

---

## Testing

### Backend Test Examples
```python
# backend/tests/test_auth.py
import pytest
from app.services.auth_service import signup_user
from app.schemas.auth import SignUpRequest

@pytest.mark.asyncio
async def test_signup_success(db):
    request = SignUpRequest(
        email="test@example.com",
        password="SecurePass123!",
        password_confirm="SecurePass123!",
        full_name="Test User",
        role="dentist"
    )
    user = await signup_user(db, request)
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"

@pytest.mark.asyncio
async def test_signup_duplicate_email(db):
    # Create first user
    request1 = SignUpRequest(...)
    await signup_user(db, request1)
    
    # Try duplicate
    request2 = SignUpRequest(email="test@example.com", ...)
    with pytest.raises(ValueError):
        await signup_user(db, request2)
```

---

## Definition of Done (Week 2 Checkpoint)

- [ ] All 9 endpoints responding correctly
- [ ] Database schema created and migrations run
- [ ] JWT authentication working (tokens valid for 30 days)
- [ ] File upload works (PDF, DOCX, images)
- [ ] Chat streaming works (tokens appear one-by-one)
- [ ] Claude API integration tested
- [ ] Stripe customer creation works
- [ ] All unit tests passing (>80% coverage)
- [ ] Frontend pages render without errors
- [ ] `docker-compose up` → full stack running
- [ ] Can signup → login → chat in browser

---

**Next**: Once approved, I begin implementation. Estimated: 2 weeks to completion.

