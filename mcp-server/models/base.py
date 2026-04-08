from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    @staticmethod
    def validate_string_length(field_name, value, min_length=2, allow_none=False):
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")

        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")

        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")

        return value
