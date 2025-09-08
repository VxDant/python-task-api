from sqlalchemy.orm import Session
from . import models, schemas


def get_task(db: Session, task_id: int):
    """Get a single task by ID"""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    """Get multiple tasks with pagination"""
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    """Create a new task"""
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    """Update an existing task"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None

    # Update only provided fields
    update_data = task.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    """Delete a task"""
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True
