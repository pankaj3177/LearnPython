from __future__ import annotations

from fastapi import FastAPI, Depends, Response, HTTPException, status, Security
from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer

from Final.models import User
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

app = FastAPI()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_current_user(
        token: str = Security(oauth2_scheme),
        db: Session = Depends(get_db)
)-> type[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if user is None:
        raise credentials_exception

    return user

@app.post("/auth/register")
def register_user(request: schemas.User, db: Session = Depends(get_db)):
    email = request.email.strip().lower()

    # Check if user already exists
    existing_user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=email, role=request.role, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")

@app.post("/auth/login")
def login(user: str,password: str, db: Session = Depends(get_db))-> models.Token:
    user = db.query(models.User).filter(models.User.email == user).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return models.Token(access_token=access_token, token_type="bearer")

@app.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email")
    return {"message": "Password reset link sent to your email"}

@app.post("/reset-password")
def reset_password(email: str, password: str,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email")
    hashed_password = pwd_context.hash(password)
    user.password = hashed_password
    db.commit()
    return {"message": "Password reset successfully"}

@app.get("/patients", response_model=list[schemas.UserResponse])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role=='Patient').offset(skip).limit(limit).all()

@app.get("/doctors", response_model=list[schemas.UserResponse])
def read_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.role=='Doctor').limit(limit).all()

@app.get("/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.get("/doctors/{id}/availability", response_model=list[schemas.AvailabilityResponse])
def read_availability(id: int, db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)):

    if current_user.role != "Doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create availability")

    doctor = db.query(models.User).filter(
        models.User.id == id,
        models.User.role == 'Doctor'
    ).first()

    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return (db.query(models.DoctorAvailability).filter(models.DoctorAvailability.doctor_id == id)
            .order_by(
                models.DoctorAvailability.date,
                models.DoctorAvailability.start_time
            ).all())

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/doctors/availability")
def create_doctor_availability(request: schemas.DoctorAvailability, db: Session = Depends(get_db),
                               current_user: models.User = Depends(get_current_user)):
    doctor = db.query(models.User).filter(models.User.id == request.doctor_id, models.User.role == 'Doctor').first()
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.add(models.DoctorAvailability(**request.model_dump()))
    db.commit()
    db.refresh(doctor)
    return {"message": "Availability created successfully"}