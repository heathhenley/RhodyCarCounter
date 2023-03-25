import requests
import sqlalchemy
import database.db_utils
import database.model as model

API = "https://rhodycarcounter-production.up.railway.app/api/cameras/"

def main():
  camera_list = requests.get(API).json()
  engine = database.db_utils.get_engine()
  model.Base.metadata.create_all(bind=engine)
  with sqlalchemy.orm.Session(engine) as session:
    for camera in camera_list:
      stm = (sqlalchemy.select(model.Camera)
        .where(model.Camera.id_from_website == camera["id_from_website"]))
      if session.scalars(stm).one_or_none():
        continue
      db_camera = model.Camera(
        id_from_website=camera["id_from_website"],
        description=camera["description"],
        name=camera["name"],
        url=camera["url"],
        latitude=camera["latitude"],
        longitude=camera["longitude"]
      )
      session.add(db_camera)
    session.commit()

if __name__ == "__main__":
  main()