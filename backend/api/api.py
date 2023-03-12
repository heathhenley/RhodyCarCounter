import sys
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from database import db_utils, model
import schema, crud

# Average and std dev cars detected (estimated used sql query of all data
# points). Hope to eventually put back camera specific values, calculated on
# the fly or cached in the db, daily or weekly maybe.
DEFAULT_AVERAGE = 16.0
DEFAULT_STD_DEV = 4.0

# Factor to use when computing status. 1.0 means everything between average
# +/- std dev is normal, 0.5 means everything between average +/- 0.5 * std dev
# is normal, etc.
DEFAULT_FACTOR = 1.0


try:
  engine = db_utils.get_engine()
  model.Base.metadata.create_all(bind=engine)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except:
  print("Failed to connect to database")
  sys.exit(1)

description = """
API to access counts from Providence, RI traffic cams. The cars are counted
using YOLOv8. I'm planning to fine tune the model to improves accuracy, it was
a pretrained model that I trained an a publically available dataset from traffic
cameras. Using data from the actual Rhode Island cameras should improve it a lot
and I also need to get a bunch of night bad weather data (it stuggles a
bit there).

The camera locations are approximate, I used the description of the location,
the feed and Google StreetView to estimate the latitute and longitude.

## Cameras
Represents a camera, stream available at the included URL. You can
**read cameras** to return all cameras or **read camera** to get info
for a single camera.

## DataPoints
You can **read datapoints** to get the number of cars found in `camera_id` at the `timestamp` (UTC)
"""


app = FastAPI(
  title="Rhody Car Counter API",
  description=description,
  contact={
    "name": "Heath Henley",
    "url": "https://github.com/heathhenley/RhodyCarCounter",
    "email": "heath.j.henley@gmail.com"
  })

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


""" Helper functions for computing status for a given camera """
def get_status(
    camera_id: int, factor=1.0,
    db: Session = Depends(get_db)) -> schema.CameraStatus:
  # TODO(Heath): Computing average and std dev per cameras is slow and the model
  # is not good enough that this extra work is worth it. I'm going to remove it
  # for now, but I'd like to add it back in the future. To put it back, just
  # compute the average and std dev and pass to compute_camera_status.
  latest = crud.get_datapoints(db, camera_id=camera_id, skip=0, limit=1)
  status = compute_camera_status(float(latest[0].vehicles), factor=factor)
  return {
    "status": status,
    "timestamp": latest[0].timestamp,
    "current": latest[0].vehicles
  }


@app.get("/")
def read_root():
  return RedirectResponse(url="/docs")


@app.get("/api/cameras/", response_model=list[schema.Camera])
def read_cameras(
    skip: int = 0, limit: int = 100, status: bool = False,
    db: Session = Depends(get_db)):
  cameras = crud.get_cameras(db, skip=skip, limit=limit)
  if status:
    for camera in cameras:
      camera.status = get_status(camera.id, factor=1.0, db=db)
  return cameras


@app.get("/api/cameras/{camera_id}", response_model=schema.Camera)
def read_camera(camera_id: int, db: Session = Depends(get_db)):
  camera = crud.get_camera(db, camera_id=camera_id)
  if camera is None:
    raise HTTPException(status_code=404, detail="Camera not found")
  camera.status = get_status(camera.id, factor=1.0, db=db)
  return camera


def compute_camera_status(
    current_count: float,
    average_count: float = DEFAULT_AVERAGE,
    std_dev: float = DEFAULT_STD_DEV,
    factor: float=0.1) -> str:
  """ Compute traffic status based on average, std dev, and current count. """
  width_of_bands = factor * std_dev
  if current_count > (average_count + width_of_bands):
    return "busy"
  if current_count < (average_count - width_of_bands):
    return "slow"
  return "normal"
 

@app.get("/api/cameras/{camera_id}/status/", response_model=schema.CameraStatus)
def read_camera_status(camera_id: int, db: Session = Depends(get_db)):
  camera = crud.get_camera(db, camera_id=camera_id)
  if camera is None:
    raise HTTPException(status_code=404, detail="Camera not found")
  return get_status(camera_id, factor=DEFAULT_FACTOR, db=db)


@app.get("/api/cameras/{camera_id}/datapoints",
  response_model=list[schema.DataPoint])
def read_datapoints(
  camera_id: int, skip: int = 0, limit: int = 1000,
  db: Session = Depends(get_db)):
  if crud.get_camera(db, camera_id=camera_id) is None:
    raise HTTPException(status_code=404, detail="Camera not found")
  return crud.get_datapoints(
    db, camera_id=camera_id, skip=skip, limit=limit)