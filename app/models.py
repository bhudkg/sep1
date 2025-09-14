from database import Base
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class PollTable(Base):
    __tablename__ = "polls"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationship to options
    options = relationship("OptionTable", back_populates="poll", cascade="all, delete-orphan")

class OptionTable(Base):
    __tablename__ = "options"
    
    id = Column(String, primary_key=True, index=True)
    option = Column(String, nullable=False)
    vote_count = Column(Integer, default=0)
    poll_id = Column(String, ForeignKey("polls.id"), nullable=False)
    
    # Relationship back to poll
    poll = relationship("PollTable", back_populates="options")
    