import os
import sqlalchemy

import database.model as model

# TODO(Heath): utils should move out of worker
import worker.utils


def get_engine(db_connect_str=os.environ.get("DB_CONNECT_STR")):
  return sqlalchemy.create_engine(db_connect_str, echo=False)

# get list of all cameras in database
def get_camera_list(engine):
  with sqlalchemy.orm.Session(engine) as session:
    stm = sqlalchemy.select(model.Camera)
    return list(session.scalars(stm))

# stick all the cameras in the database
def upsert_cameras_bulk(engine, camera_list):
  with sqlalchemy.orm.Session(engine) as session:
    for camera in camera_list:
      stm = (sqlalchemy.select(model.Camera)
        .where(model.Camera.id_from_website == camera["id"]))
      if session.scalars(stm).one_or_none():
        continue
      db_camera = model.Camera(
        id_from_website=camera["id"],
        description=camera["description"],
        name=camera["name"],
        url=camera["link"]
      )
      session.add(db_camera)
    session.commit()

def insert_data(camera_id, timestamp, image_name, vehicles, engine):
  # make a data point
  with sqlalchemy.orm.Session(engine) as session:
    session.add(model.DataPoint(
      camera_id=camera_id,
      vehicles=vehicles,
      timestamp=timestamp
    ))
    session.commit()

def main():
  engine = get_engine()
  model.Base.metadata.create_all(bind=engine)

  print("Upsert!")
  # insert cameras if not in db
  upsert_cameras_bulk(
    engine,
    worker.utils.get_cams_from_page(worker.utils.CAM_LIST_URL))

  print("Query them back!")
  # print them back out
  print(get_camera_list(engine))


if __name__ == "__main__":
  main()