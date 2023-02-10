import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Camera(Base):
    __tablename__ = "camera"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_from_website: Mapped[str]
    description: Mapped[str]
    name: Mapped[Optional[str]]
    url: Mapped[str]

    def __repr__(self) -> str:
        return f""

class DataPoint(Base):
    __tablename__ = "vehicle_frequency_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey("camera.id"))
    vehicles: Mapped[int]
    timestamp: Mapped[datetime.datetime]

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"