# Development Guide

## Development Setup

### Backend Development

#### Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run Locally

```bash
# Set up environment
cp .env.example .env

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

#### Add New Dependencies

```bash
pip install package_name
pip freeze > requirements.txt
git add requirements.txt && git commit -m "Add new dependency"
```

### Frontend Development

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Run Locally

```bash
# Set up environment
cp .env.example .env

# Start dev server
npm run dev
```

Dev server runs on `http://localhost:3000`

#### Build for Production

```bash
npm run build    # Creates dist/
npm run preview  # Preview production build locally
```

## Code Style & Formatting

### Backend (Python)

**Style Guide**: PEP 8

```bash
# Format code
black app/

# Check style
pylint app/

# Type checking
mypy app/
```

**Code Style Rules**:
- Line length: 88 characters (black default)
- Imports: Organized (stdlib, third-party, local)
- Naming: snake_case for functions/variables, PascalCase for classes
- Docstrings: Google-style docstrings for public functions

### Frontend (TypeScript)

**Style Guide**: ESLint + Prettier

```bash
# Format code
npm run format

# Lint code
npm run lint

# Fix lint errors
npm run lint -- --fix
```

**Code Style Rules**:
- 2 spaces indentation
- Semicolons: Required
- Quotes: Single quotes for JS, double for JSX attributes
- Components: PascalCase, hooks: camelCase with "use" prefix

## Adding a New Feature

### Example: Adding a New API Endpoint

#### 1. Define the Model (if needed)

```python
# backend/app/models/my_model.py
from sqlalchemy import Column, String
from app.database import Base

class MyModel(Base):
    __tablename__ = "my_models"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
```

#### 2. Create a Pydantic Schema

```python
# backend/app/schemas/my_schema.py
from pydantic import BaseModel
from typing import Optional

class MyModelCreate(BaseModel):
    name: str

class MyModelRead(BaseModel):
    id: str
    name: str
    
    class Config:
        from_attributes = True
```

#### 3. Add Business Logic (Service)

```python
# backend/app/services/my_service.py
from sqlalchemy.orm import Session
from app.models.my_model import MyModel

def create_my_model(db: Session, data: dict):
    db_model = MyModel(**data)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model
```

#### 4. Create Route/Endpoint

```python
# backend/app/routes/my_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.my_schema import MyModelCreate, MyModelRead
from app.services.my_service import create_my_model

router = APIRouter()

@router.post("/my-models/", response_model=MyModelRead)
def create_model(data: MyModelCreate, db: Session = Depends(get_db)):
    return create_my_model(db, data.dict())
```

#### 5. Include Router in Main App

```python
# backend/app/main.py
from app.routes import my_routes

app.include_router(
    my_routes.router,
    prefix=settings.api_v1_prefix + "/my-models",
    tags=["my-models"]
)
```

#### 6. Test the Endpoint

```python
# backend/tests/test_my_routes.py
def test_create_model(client):
    response = client.post(
        "/api/v1/my-models/",
        json={"name": "Test Model"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Model"
```

### Example: Adding a Frontend Component

#### 1. Create Component

```typescript
// frontend/src/components/MyComponent.tsx
import React from 'react'

interface Props {
  title: string
  onAction: () => void
}

export const MyComponent: React.FC<Props> = ({ title, onAction }) => {
  return (
    <div className="p-4 border rounded-lg">
      <h2 className="text-lg font-bold">{title}</h2>
      <button 
        onClick={onAction}
        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Action
      </button>
    </div>
  )
}
```

#### 2. Use in Page

```typescript
// frontend/src/pages/MyPage.tsx
import { MyComponent } from '../components/MyComponent'

export const MyPage = () => {
  const handleAction = () => {
    console.log('Action triggered')
  }

  return (
    <div className="container mx-auto">
      <MyComponent 
        title="My Component" 
        onAction={handleAction}
      />
    </div>
  )
}
```

#### 3. Add Route

```typescript
// frontend/src/App.tsx
import { MyPage } from './pages/MyPage'

// In Routes:
<Route path="/my-page" element={<MyPage />} />
```

## Testing

### Running Tests

```bash
# Backend - all tests
cd backend
pytest

# Backend - specific test file
pytest tests/test_auth.py

# Backend - with coverage
pytest --cov=app

# Frontend - all tests
cd frontend
npm test

# Frontend - watch mode
npm test -- --watch
```

### Writing Tests

#### Backend Test Example

```python
# backend/tests/test_my_service.py
import pytest
from sqlalchemy.orm import Session
from app.services.my_service import create_my_model

def test_create_my_model(db: Session):
    data = {"name": "Test"}
    result = create_my_model(db, data)
    
    assert result.name == "Test"
    assert result.id is not None
```

#### Frontend Test Example

```typescript
// frontend/src/components/__tests__/MyComponent.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { MyComponent } from '../MyComponent'

test('renders and handles click', () => {
  const handleClick = vi.fn()
  render(<MyComponent title="Test" onAction={handleClick} />)
  
  const button = screen.getByRole('button')
  fireEvent.click(button)
  
  expect(handleClick).toHaveBeenCalled()
})
```

## Database Migrations

### Create Migration

```bash
cd backend

# Auto-generate from models
alembic revision --autogenerate -m "Add my_models table"

# Or create empty migration
alembic revision -m "Add my_models table"
```

Edit `alembic/versions/xxx_add_my_models_table.py` to define migration.

### Apply Migrations

```bash
# Apply all pending
alembic upgrade head

# Rollback one
alembic downgrade -1

# Rollback to specific
alembic downgrade <revision>
```

## Git Workflow

### Branch Naming

```
feature/user-auth              # New feature
fix/chat-message-bug           # Bug fix
refactor/extract-service       # Refactoring
docs/api-documentation         # Documentation
chore/update-dependencies      # Maintenance
```

### Commit Messages

```
feat: Add user authentication endpoint
fix: Resolve chat message ordering issue
refactor: Extract email service to separate module
docs: Update API documentation
chore: Upgrade FastAPI to 0.105.0
```

**Format**: `<type>: <subject>`

### Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test locally
3. Commit changes: `git commit -m "feat: Add my feature"`
4. Push to remote: `git push origin feature/my-feature`
5. Open PR on GitHub
6. Request reviews
7. Address feedback
8. Merge when approved

## Docker Development

### Rebuild Images

```bash
docker-compose build
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Execute Commands in Container

```bash
# Backend shell
docker-compose exec backend bash

# Run migrations
docker-compose exec backend alembic upgrade head

# Frontend npm
docker-compose exec frontend npm install
```

### Reset Database

```bash
# Stop and remove containers, volumes
docker-compose down -v

# Restart (will reinitialize DB)
docker-compose up
```

## Debugging

### Backend Debugging

#### Using print/logging

```python
import logging

logger = logging.getLogger(__name__)
logger.debug(f"Variable: {my_var}")
logger.info("User logged in")
logger.error("An error occurred")
```

#### Using debugger (pdb)

```python
import pdb; pdb.set_trace()  # Stop here
```

#### VS Code Debug Configuration

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging

#### Browser DevTools

- Open Chrome DevTools (F12)
- Network tab: See API calls
- Console tab: See errors/logs
- React DevTools extension: Inspect component tree

#### VSCode Debugger

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch React App",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

## Performance Optimization

### Backend

- Use database indexes for frequent queries
- Implement caching (Redis) for expensive operations
- Use pagination for large result sets
- Monitor query performance (SQLAlchemy logging)

### Frontend

- Lazy load routes
- Optimize images (use WebP, appropriate sizes)
- Use React.memo for expensive components
- Minimize bundle size (tree-shaking, code splitting)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | `lsof -i :8000` then kill process or use different port |
| Database connection refused | Ensure `docker-compose up` is running postgres |
| CORS errors | Check `allowed_origins` in backend config |
| Frontend can't reach backend | Verify `REACT_APP_API_URL` in .env file |
| Node modules issues | `rm -rf node_modules && npm install` |
| Python dependencies conflict | `pip install --upgrade -r requirements.txt` |

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)

---

**Last Updated**: 2026-06-22
