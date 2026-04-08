from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from .base import BaseModel


class Breed(BaseModel):
    __tablename__ = 'breeds'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    dogs = relationship('Dog', backref='breed_info', lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        return self.validate_string_length('Breed name', name, min_length=2)

    @validates('description')
    def validate_description(self, key, description):
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self):
        return f'<Breed {self.name}>'
