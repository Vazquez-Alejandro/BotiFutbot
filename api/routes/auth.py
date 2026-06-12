import hmac
import hashlib
import time
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from shared.database import get_db
from shared.models import Usuario
from api.config import get_settings

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()


class TelegramAuthRequest(BaseModel):
    id: int
    first_name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


def verify_telegram_auth(data: dict, bot_token: str) -> bool:
    check_hash = data.pop("hash", None)
    if not check_hash:
        return False

    data_check = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()

    if computed_hash != check_hash:
        return False

    auth_age = int(time.time()) - int(data.get("auth_date", 0))
    if auth_age > 86400:
        return False

    return True


@router.post("/telegram")
def auth_telegram(payload: TelegramAuthRequest, db: Session = Depends(get_db)):
    data = payload.dict()
    if not verify_telegram_auth(data, settings.TELEGRAM_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid Telegram auth")

    usuario = db.query(Usuario).filter(Usuario.telegram_id == payload.id).first()
    if not usuario:
        usuario = Usuario(
            telegram_id=payload.id,
            username=payload.username,
            first_name=payload.first_name,
            photo_url=payload.photo_url,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    token = hmac.new(
        settings.JWT_SECRET.encode(),
        str(usuario.id).encode(),
        hashlib.sha256,
    ).hexdigest()

    return {
        "token": token,
        "user": {
            "id": usuario.id,
            "telegram_id": usuario.telegram_id,
            "username": usuario.username,
            "first_name": usuario.first_name,
            "photo_url": usuario.photo_url,
        }
    }


def get_current_user(db: Session = Depends(get_db), token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = int(hmac.new(settings.JWT_SECRET.encode(), token.encode(), hashlib.sha256).hexdigest(), 16) % 100000
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="User not found")
    return usuario
