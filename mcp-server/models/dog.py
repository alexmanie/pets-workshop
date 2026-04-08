from datetime import datetime
from enum import Enum
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import validates, Mapped, mapped_column
from .base import BaseModel


class AdoptionStatus(Enum):
    AVAILABLE = 'Available'
    ADOPTED = 'Adopted'
    PENDING = 'Pending'


class Dog(BaseModel):
    __tablename__ = 'dogs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    breed_id: Mapped[int | None] = mapped_column(Integer, ForeignKey('breeds.id'))
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[AdoptionStatus] = mapped_column(
        SAEnum(AdoptionStatus), default=AdoptionStatus.AVAILABLE
    )
    intake_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    adoption_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        return self.validate_string_length('Dog name', name, min_length=2)

    @validates('gender')
    def validate_gender(self, key, gender):
        if gender not in ['Male', 'Female', 'Unknown']:
            raise ValueError("Gender must be 'Male', 'Female', or 'Unknown'")
        return gender

    @validates('description')
    def validate_description(self, key, description):
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description

    def __repr__(self):
        return f'<Dog {self.name}, ID: {self.id}, Status: {self.status.value}>'
