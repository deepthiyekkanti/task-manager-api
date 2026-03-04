from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    UserCreate, UserResponse,
    LoginRequest, LoginResponse,
    MeResponse,
    RefreshTokenRequest, RefreshTokenResponse,
    LogoutRequest
)
from services.user_service import UserService
from services.auth_service import AuthService
from auth.deps import get_current_user_id

from rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

user_service = UserService()
auth_service = AuthService()


@router.post("/signup", response_model=UserResponse)
@limiter.limit("3/minute")
def signup(request: Request, user: UserCreate, db: Session = Depends(get_db)):
        return user_service.signup(db, user)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
def login(request: Request, creds: LoginRequest, db: Session = Depends(get_db)):
    tokens = auth_service.login(db, creds.email, creds.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return tokens


@router.get("/me", response_model=MeResponse)
def me(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return user_service.get_me(db, user_id)


@router.post("/refresh", response_model=RefreshTokenResponse)
@limiter.limit("10/minute")
def refresh(request: Request, payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    tokens = auth_service.refresh_access_token(db, payload.refresh_token)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return tokens


@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    ok = auth_service.logout(db, payload.refresh_token)
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {"message": "Logged out successfully"}