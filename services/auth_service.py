from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models import User, RefreshToken
from auth.security import verify_password
from auth.jwt_handler import create_access_token, generate_refresh_token, hash_refresh_token


class AuthService:
    def login(self, db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        # revoke existing refresh tokens (single-session policy)
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id,
            RefreshToken.revoked == False
        ).update({"revoked": True}, synchronize_session=False)

        access_token = create_access_token({"user_id": user.id})

        raw_refresh, expires_at = generate_refresh_token()
        refresh_hash = hash_refresh_token(raw_refresh)

        db.add(
            RefreshToken(
                user_id=user.id,
                token_hash=refresh_hash,
                expires_at=expires_at,
                revoked=False,
            )
        )

        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh,
            "token_type": "bearer",
        }

    def refresh_access_token(self, db: Session, refresh_token: str):
        token_hash = hash_refresh_token(refresh_token)

        token_row = (
            db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked == False,
            )
            .first()
        )
        if not token_row:
            return None

        now = datetime.now(timezone.utc)

        # If expired, revoke it so it can never be reused / keeps DB clean
        if token_row.expires_at < now:
            token_row.revoked = True
            db.commit()
            return None

        # Rotation: revoke old refresh token
        token_row.revoked = True

        # Create new refresh token
        raw_refresh, expires_at = generate_refresh_token()
        refresh_hash = hash_refresh_token(raw_refresh)

        db.add(
            RefreshToken(
                user_id=token_row.user_id,
                token_hash=refresh_hash,
                expires_at=expires_at,
                revoked=False,
            )
        )

        # Mint new access token
        new_access = create_access_token({"user_id": token_row.user_id})

        db.commit()

        return {
            "access_token": new_access,
            "refresh_token": raw_refresh,
            "token_type": "bearer",
        }

    def logout(self, db: Session, refresh_token: str) -> bool:
        token_hash = hash_refresh_token(refresh_token)

        token_row = (
            db.query(RefreshToken)
            .filter(RefreshToken.token_hash == token_hash, RefreshToken.revoked == False)
            .first()
        )
        if not token_row:
            return False

        token_row.revoked = True
        db.commit()
        return True