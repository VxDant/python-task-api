from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Import your modules
from . import crud, models, schemas
from .database import engine, get_db  # Import get_db here
from .security import verify_api_key, verify_admin_key, get_current_user, api_usage

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Environment-based configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ENABLE_DOCS = os.getenv("ENABLE_DOCS", "true").lower() == "true"

app = FastAPI(
    title="Task Management API",
    description="A secure task management system for CI/CD demonstration",
    version="1.0.0",
    docs_url="/docs" if ENABLE_DOCS else None,
    redoc_url="/redoc" if ENABLE_DOCS else None,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ENVIRONMENT == "development" else ["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Public health check (for Cloud Run health checks)
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "docs_enabled": ENABLE_DOCS
    }

# Root endpoint with API key protection
@app.get("/", dependencies=[Depends(verify_api_key)])
def read_root(request: Request):
    return {
        "message": "Task Management API",
        "status": "authenticated",
        "docs_url": "/docs" if ENABLE_DOCS else "disabled",
        "api_key_type": request.state.api_key_type
    }

# Protected task endpoints
@app.post("/tasks/", response_model=schemas.Task, dependencies=[Depends(verify_api_key)])
def create_task(
    request: Request,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)  # Now get_db is properly imported
):
    return crud.create_task(db=db, task=task)

@app.get("/tasks/", response_model=list[schemas.Task], dependencies=[Depends(verify_api_key)])
def read_tasks(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)  # get_db working now
):
    return crud.get_tasks(db, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=schemas.Task, dependencies=[Depends(verify_api_key)])
def read_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.put("/tasks/{task_id}", response_model=schemas.Task, dependencies=[Depends(verify_api_key)])
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", dependencies=[Depends(verify_api_key)])
def delete_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# Admin endpoint to monitor API usage
@app.get("/admin/usage", dependencies=[Depends(verify_admin_key)])
def get_api_usage():
    """Admin endpoint to view API usage statistics"""
    return {
        "total_usage": api_usage,
        "active_sessions": len(api_usage),
        "endpoint": "admin_only"
    }

# Optional: User info endpoint
@app.get("/me", dependencies=[Depends(verify_api_key)])
def get_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information based on API key"""
    return current_user
