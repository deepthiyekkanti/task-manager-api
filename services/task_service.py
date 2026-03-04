from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from fastapi import HTTPException
from models import Task
from schemas import TaskCreate, TaskUpdate


class TaskService:
    def create_task(self, db: Session, task: TaskCreate, user_id: int):
        new_task = Task(
            title=task.title,
            description=task.description,
            completed= False,
            user_id=user_id,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    def get_tasks(self, db: Session, user_id: int, completed: bool | None,
    search: str | None, sort: str, order: str, page: int, page_size: int,):
        
    # ---- Input validation (strict) ----
        if page < 1:
            raise HTTPException(status_code=422, detail="page must be >= 1")

        # choose a sensible max to prevent abuse
        MAX_PAGE_SIZE = 100
        if page_size < 1 or page_size > MAX_PAGE_SIZE:
            raise HTTPException(
                status_code=422,
                detail=f"page_size must be between 1 and {MAX_PAGE_SIZE}",
            )

        allowed_sort_fields = {
            "created_at": Task.created_at,
            "updated_at": Task.updated_at,
            "title": Task.title,
            "completed": Task.completed,
            "id": Task.id,
        }
        if sort not in allowed_sort_fields:
            raise HTTPException(status_code=422, detail="Invalid sort field")

        if order not in ("asc", "desc"):
            raise HTTPException(status_code=422, detail="Invalid order (must be asc or desc)")

        # ---- Base query (user-scoped) ----
        query = db.query(Task).filter(Task.user_id == user_id)

        if completed is not None:
            query = query.filter(Task.completed == completed)

        # ---- Search (NULL-safe) ----
        if search:
            like = f"%{search}%"
            query = query.filter(
                or_(
                    Task.title.ilike(like),
                    func.coalesce(Task.description, "").ilike(like),
                )
            )

        # ---- Total before pagination ----
        total = query.count()

        # ---- Sorting (allowlisted + stable pagination) ----
        sort_column = allowed_sort_fields[sort]

        if order == "desc":
            query = query.order_by(sort_column.desc(), Task.id.desc())
        else:
            query = query.order_by(sort_column.asc(), Task.id.asc())

        # ---- Pagination ----
        offset = (page - 1) * page_size
        tasks = query.offset(offset).limit(page_size).all()

        return {
            "data": tasks,
            "meta": {"page": page, "page_size": page_size, "total": total},
        }

    def get_task_by_id(self, db: Session, task_id: int, user_id: int):
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def update_task(self, db: Session, task_id: int, update: TaskUpdate, user_id: int):
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if update.title is not None:
            task.title = update.title
        if update.description is not None:
            task.description = update.description
        if update.completed is not None:
            task.completed = update.completed

        db.commit()
        db.refresh(task)
        return task

    def delete_task(self, db: Session, task_id: int, user_id: int):
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()