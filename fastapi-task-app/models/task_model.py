from sqlalchemy import Column, String, Text
from database.database import Base  # Ensure this matches your `Base` definition

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="pending")
    result = Column(Text, nullable=True)
