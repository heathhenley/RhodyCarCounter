import datetime
from pydantic import BaseModel


class DataPoint(BaseModel):
  id: int
  camera_id: int
  vehicles: int
  timestamp: datetime.datetime

  class Config:
    orm_mode = True


class Camera(BaseModel):
  id: int
  id_from_website: str
  description: str
  name: str
  url: str
  latitude: float | None
  longitude: float | None

  class Config:
    orm_mode = True



