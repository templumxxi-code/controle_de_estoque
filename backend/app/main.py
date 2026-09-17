from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.api.routes import router
from app.db.session import Base, engine
from app.core.config import settings
from app.core.security import hash_password
from app.models import User
from app.db.session import SessionLocal
import app.models  # noqa: F401


def ensure_user_schema() -> None:
    if "users" not in inspect(engine).get_table_names():
        return
    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    additions = {
        "is_admin": "BOOLEAN NOT NULL DEFAULT FALSE",
        "full_name": "VARCHAR(180) NULL",
        "phone": "VARCHAR(40) NULL",
        "job_title": "VARCHAR(120) NULL",
        "role": "VARCHAR(30) NOT NULL DEFAULT 'operator'",
        "must_change_password": "BOOLEAN NOT NULL DEFAULT FALSE",
        "last_login_at": "DATETIME NULL",
        "theme_preference": "VARCHAR(10) NOT NULL DEFAULT 'dark'",
        "updated_at": "DATETIME NULL",
    }
    with engine.begin() as connection:
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(text(f"ALTER TABLE users ADD COLUMN {name} {definition}"))


def ensure_admin_user() -> None:
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == settings.admin_email.lower().strip()).first()
        if user:
            if not user.is_admin:
                user.is_admin = True
            user.role = "admin"
            user.full_name = user.full_name or "Administrador Pumphouseup"
            user.theme_preference = user.theme_preference or "dark"
            db.commit()
            return
        db.add(User(email=settings.admin_email.lower().strip(), password_hash=hash_password(settings.admin_password), is_admin=True, role="admin", full_name="Administrador Pumphouseup"))
        db.commit()

@asynccontextmanager
async def lifespan(_: FastAPI):
    ensure_user_schema()
    Base.metadata.create_all(bind=engine)
    ensure_admin_user()
    yield


app = FastAPI(title="Pumphouseup API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
