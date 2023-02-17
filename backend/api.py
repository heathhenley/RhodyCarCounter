import sys
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, sessionmaker
from database import db_utils, model
import schema, crud

try:
  engine = db_utils.get_engine()
  model.Base.metadata.create_all(bind=engine)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except:
  print("Failed to connect to database")
  sys.exit(1)

description = """
API to access counts from Providence, RI traffic cams. The cars are counted
using YOLOv2. I'm planning to fine tune the model, params were trained on self
driving car data so it's not perfect. The model itself was adapted from
the Coursera deep learning course project on the Yolo model.

## Cameras
Represents a camera, stream available at the included URL. You can
**read cameras** to return all cameras or **read camera** to get info
for a single camera.

## DataPoints
You can **read datapoints** to get the number of cars found in `camera_id` at the `timestamp` (UTC)
"""


app = FastAPI(
  title="Providence Traffic Cam API",
  description=description,
  contact={
    "name": "Heath Henley",
    "url": "https://github.com/heathhenley/RhodyCarCounter",
    "email": "heath.j.henley@gmail.com"
  })


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/")
def read_root():
  return RedirectResponse(url="/docs")

@app.get("/api/cameras/", response_model=list[schema.Camera])
def read_cameras(
  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  cameras = crud.get_cameras(db, skip=skip, limit=limit)
  return cameras

@app.get("/api/cameras/{camera_id}", response_model=schema.Camera)
def read_camera(camera_id: int, db: Session = Depends(get_db)):
  camera = crud.get_camera(db, camera_id=camera_id)
  if camera is None:
    raise HTTPException(status_code=404, detail="Camera not found")
  return camera

@app.get("/api/cameras/{camera_id}/datapoints",
  response_model=list[schema.DataPoint])
def read_datapoints(
  camera_id: int, skip: int = 0, limit: int = 1000,
  db: Session = Depends(get_db)):
  if crud.get_camera(db, camera_id=camera_id) is None:
    raise HTTPException(status_code=404, detail="Camera not found")
  return crud.get_datapoints(
    db, camera_id=camera_id, skip=skip, limit=limit)