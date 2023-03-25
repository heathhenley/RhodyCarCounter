""" Use Yolo model to count cars seen on PVD traffic cams """
import datetime
import os
import requests
import time

import boto3
from ultralytics import YOLO

import database.db_utils as db_utils

S3_BUCKET = 'rhodycarcounter'

# Download image to disk for the given camera, return friendlier name
def download_image(url: str, cam_name: str):
  # NOTE(Heath) use PIL or IO to keep in RAM, disk is going to be slow, though
  # it still might be ok with the number of cameras we have as they're only
  # updating their images roughly every minute - so it might not actually
  # matter yet.
  try:
    res = requests.get(url, timeout=0.500)
  except Exception as e:
    print(f"{e}")
    return None
  if res.status_code != 200:
    print(res.status_code)
    return None
  image_name = f"{cam_name.lower().replace('/', '_')}.jpg"
  with open(f"images/{image_name}", 'wb') as f:
    f.write(res.content)
  return image_name


# This is the main "service" - just loop indefinitely and grab traffic cam pics,
# YOLO them, and stick results in a database - currently thinking it could be
# completely standalone and hit an api to submit the data. Maybe overkill for
# MVP, TBD
def detect_vehicles(data_callback=None):
  # Load model
  model_path = os.path.dirname(os.path.realpath(__file__))
  yolo_model = YOLO(
    os.path.join(model_path, "train_13epochs_on_traffic_gpu.pt"), task='detect')
  # Some setup
  if not os.path.exists("images"):
    os.makedirs("images")
  s3 = boto3.resource('s3')
  engine = db_utils.get_engine()
  cameras = db_utils.get_camera_list(engine)
  while True:
    # This whole step could be processed independently for each url
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    for camera in cameras:
      total_process_time_tic = time.perf_counter()
      camera_name, url = camera.name, camera.url
      # Get image from server
      # Also not sure whether we want to overwrite each time (as we are doing
      #  now) or save the images with a timestamp, or save the input image with
      # the bounding box predictions, tbd
      image_name = download_image(url, camera_name)
      if image_name is None:
        print(f"Fail to get image: {image_name} ")
        continue

      # Run prediction
      tic = time.perf_counter()
      results = yolo_model.predict(
        f"images/{image_name}", save=True, exist_ok=True)
      vehicles = results[0].boxes.cls.shape[0]
      print(f"  Prediction Time: {time.perf_counter() - tic} secs")

      if data_callback:
        data_callback(
          camera.id, timestamp, image_name, vehicles, engine)

      # TODO(Heath) fix image path and hacky close / open, global s3 name
      try:
        with open(os.path.join('runs/detect/predict', image_name), 'rb') as f:
          s3.Bucket(S3_BUCKET).put_object(
            Key=image_name, Body=f,
            ContentType='image/jpeg',
            CacheControl='max-age=300')
      except Exception as e:
        print("Failed to put in s3 bucket")
        print(e)

      print(
        f"  Total Time to Process/Insert: {time.perf_counter() - total_process_time_tic} secs")
    # Adjust to not run the same frame too many times, the pics only update
    # roughly every minute or so. With ~50 cams taking 0.5 secs each to
    # process, that's still only 25 seconds, so we can take a little break to
    # avoid too many duplicate runs. It will also reduce cost if the db or
    # or worker is too expensive
    time.sleep(60 * 5) # running every 5 minutes

def main():
  print("Starting traffic worker")
  detect_vehicles(data_callback=db_utils.insert_data)

if __name__ == "__main__":
  main()