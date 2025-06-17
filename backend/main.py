from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

DATABASE_URL = 'sqlite:///./interview_app.db'

engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Interview(Base):
    __tablename__ = 'interviews'
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    scheduled_time = Column(DateTime)
    duration_minutes = Column(Integer)
    link = Column(String)
    status = Column(String, default='Scheduled')
    candidate = relationship('Candidate')

class Availability(Base):
    __tablename__ = 'availability'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    is_booked = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

class ScheduleRequest(BaseModel):
    candidate_id : int
    scheduled_time : datetime
    duration_minutes : int

class RescheduleRequest(BaseModel):
    interview_id : int
    new_time : datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_email(to_address: str, subject: str, body: str):
    from_address = 'your-email@example.com'
    password = 'your-email-password'

    msg = MIMEMultipart()
    msg['FROM'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())

@app.post("/schedule")
def schedule_interview(request: ScheduleRequest, db: SessionLocal = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == request.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    interview = Interview(
        candidate_id = request.candidate_id,
        scheduled_time = request.scheduled_time,
        duration_minutes = request.duration_minutes,
        link = "http://example.com/interview-link"
    )
    db.add(interview)
    db.commit()

    email_body = f"Dear {candidate.name},\n\nYour interview is scheduled at {request.scheduled_time} for {request.duration_minutes} minutes.\nLink: http://example.com/interview-link"
    send_email(candidate.email, "Interview scheduled", email_body)

    host_email = "host-email@example.com"
    host_body = f"Interview scheduled with {candidate.name} ({candidate.email}) at {request.scheduled_time}."
    send_email(host_email, "New Interview Scheduled", host_body)

    return {"message": "Interview scheduled successfully"}


@app.put('/reschedule')
def reschedule_interview(request: RescheduleRequest, db: SessionLocal = Depends(get_db)):
    interview = db.query(Interview).filter(Interview.id == request.interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    interview.scheduled_time = request.new_time
    db.commit()

    candidate = interview.cadidate
    email_body = f"Dear {candidate.name},\n\nYour interview has been rescheduled to {request.new_time}.\nLink: {interview.link}"
    send_email(candidate.email, "Interview Rescheduled", email_body)

    host_email = "host-email@example.com"
    host_body = f"Interview rescheduled with {candidate.name} ({candidate.email}) to {request.new_time}."
    send_email(host_email, "Interview Rescheduled", host_body)

    return {"message":"Interview Rescheduled Successfully"}