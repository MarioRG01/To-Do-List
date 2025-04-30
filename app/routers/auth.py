from fastapi import APIRouter, Depends, HTTPException, status
from app.db.base import database
from app.db.models import users
from app.schemas.user import UserCreate, UserRead, Token
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate):
    # Verificar que no exista el email
    exists = await database.fetch_one(users.select().where(users.c.email == user.email))
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Crear usuario
    hashed = hash_password(user.password)
    insert = users.insert().values(email=user.email, hashed_password=hashed)
    user_id = await database.execute(insert)
    return {"id": user_id, "email": user.email}

@router.post("/login", response_model=Token)
async def login(form_data: UserCreate):
    # Cargar usuario
    db_user = await database.fetch_one(users.select().where(users.c.email == form_data.email))
    if not db_user or not verify_password(form_data.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generar JWT
    token = create_access_token({"user_id": db_user["id"]})
    return {"access_token": token, "token_type": "bearer"}
