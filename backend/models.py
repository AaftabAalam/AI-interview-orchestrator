from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    interviews = relationship('Interview', back_populates="candidate")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    scheduled_time = Column(DateTime)
    duration_minutes = Column(Integer)
    link = Column(String)
    status = Column(String, default="Scheduled")

    candidate = relationship("Candidate", back_populates="interviews")

class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    is_booked = Column(Boolean, default=False)
