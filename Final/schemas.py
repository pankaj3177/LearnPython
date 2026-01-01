from pydantic import BaseModel, EmailStr, SecretStr
from datetime import date, time

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # "doctor" | "patient"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

class DoctorAvailability(BaseModel):
    doctor_id: int
    date: date
    start_time: time
    end_time: time

class AvailabilityResponse(BaseModel):
    id: int
    date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True