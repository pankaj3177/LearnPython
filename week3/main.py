from fastapi import FastAPI, Depends, Response, HTTPException
from typing import Optional
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/user")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f" {new_user.name} created successfully"}

@app.post("/login")
def login(request: schemas.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"message": "Logged in successfully"}

@app.get("/users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()

@app.post("/logout")
def logout():
    return {"message": "Logged out successfully"}