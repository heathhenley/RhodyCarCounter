from sqlalchemy.orm import Session
from sqlalchemy import func

from database import model
import schema

def get_camera(db: Session, camera_id: int):
  return (db.query(model.Camera)
          .filter(model.Camera.id == camera_id).first())

def get_cameras(db: Session, skip: int = 0, limit: int = 100):
  return db.query(model.Camera).offset(skip).limit(limit).all()

def get_datapoints(
  db: Session, camera_id: int, skip: int = 0, limit: int = 1000):
  return (db.query(model.DataPoint)
          .filter(model.DataPoint.camera_id == camera_id)
          .order_by(model.DataPoint.timestamp.desc()).offset(skip)
          .limit(limit).all())

def get_average(
    db: Session, camera_id: int, limit: int = 1000) ->tuple[float, float]:
  avg, std = (db.query(
    func.avg(model.DataPoint.vehicles),
    func.stddev(model.DataPoint.vehicles))
    .filter(model.DataPoint.camera_id == camera_id)
    .limit(limit).first())
  return float(avg), float(std)

def get_camera(db: Session, camera_id: int):
  return (db.query(model.Camera)
          .filter(model.Camera.id == camera_id).first())