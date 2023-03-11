import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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
    latitude: Mapped[Optional[float]]
    longitude: Mapped[Optional[float]]

    def __repr__(self) -> str:
        return f"Name(name={self.name!r})"

class DataPoint(Base):
    __tablename__ = "vehicle_frequency_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey("camera.id"))
    vehicles: Mapped[int]
    timestamp: Mapped[datetime.datetime]

    def __repr__(self) -> str:
        return f"Timestamp(time={self.timestamp!r}), Cam(camera_id={self.camera_id!r}), Vehicles(vehicles={self.vehicles!r})"