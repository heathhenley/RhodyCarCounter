from sqlalchemy.orm import Session

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