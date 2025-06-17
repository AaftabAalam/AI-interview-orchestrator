from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleRequest(BaseModel):
    candidate_id : int
    scheduled_time : datetime
    duration_minutes : int

class RescheduleRequest(BaseModel):
    interview_id : int
    new_time : datetime

class CandidateResponse(BaseModel):
    id : int
    name : str
    email : str

    class Config:
        orm_mode = True

class InterviewResponse(BaseModel):
    id : int
    candidate_id : int
    scheduled_time : datetime
    duration_minutes : int
    link : str
    status : str

    class Config:
        orm_mode = True