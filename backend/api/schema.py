import datetime
from pydantic import BaseModel

class CameraStatus(BaseModel):
  status: str
  current: int
  timestamp: datetime.datetime
  average: float | None
  std_dev: float | None


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
  status: CameraStatus | None

  class Config:
    orm_mode = True