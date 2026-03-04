from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import TaskCreate, TaskUpdate, TaskResponse, PaginatedTaskResponse
from services.task_service import TaskService
from auth.deps import get_current_user_id

router = APIRouter(prefix="/tasks", tags=["Tasks"])
task_service = TaskService()


@router.post("", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.create_task(db, task, user_id)


@router.get("", response_model=PaginatedTaskResponse)
def get_tasks(
    completed: bool | None = None,
    search: str | None = None,
    sort: str = "created_at",
    order: str = "asc",
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.get_tasks(db, user_id, completed, search, sort, order, page, page_size)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.get_task_by_id(db, task_id, user_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    update: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return task_service.update_task(db, task_id, update, user_id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    # MUST call the service
    task_service.delete_task(db, task_id, user_id)

    # Return 204 with no body
    return Response(status_code=status.HTTP_204_NO_CONTENT)