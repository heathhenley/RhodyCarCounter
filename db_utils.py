import sqlalchemy

import model


def get_camera_list(engine):
  with sqlalchemy.orm.Session(engine) as session:
    stm = sqlalchemy.select(model.Camera)
    for cam in session.scalars(stm):
      print(cam)

def main(engine):
  # Get test session
  model.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
  engine = sqlalchemy.create_engine("sqlite://", echo=True)
  main(engine)
  get_camera_list(engine)