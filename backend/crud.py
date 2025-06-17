from sqlalchemy.orm import Session
from datetime import datetime
from models import Candidate, Interview, Availability
import schemas

def get_candidate_by_email(db: Session, email: str):
    return db.query(Candidate).filter(Candidate.email == email).first()

def get_candidate_by_id(db: Session, candidate_id: int):
    return db.query(Candidate).filter(Candidate.id == candidate_id).first()

def create_interview(db: Session, interview: schemas.ScheduleRequest, interview_link: str):
    db_interview = Interview(
        candidate_id = interview.candidate_id,
        scheduled_time = interview.scheduled_time,
        duration_minutes = interview.duration_minutes,
        link = interview_link,
        status = "Scheduled"
    )

    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview


def update_interview_schedule(db: Session, interview_id: int, new_time: datetime):
    db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if db_interview:
        db_interview.scheduled_time = new_time
        db_interview.status = "Recheduled"
        db.commit()
        db.refresh(db_interview)

    return db_interview

def get_available_slots(db: Session):
    return db.query(Availability).filter(Availability.is_booked == False).all()

def book_slot(db: Session, availability_id: int):
    slot = db.query(Availability).filter(Availability.id == availability_id).first()
    if slot:
        slot.is_booked = True
        db.commit()
    return slot