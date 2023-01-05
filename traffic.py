import datetime
import requests
import time
from yolo import YoloModel, save_image_with_boxes

import utils

SAVE_IMAGE = True # debug (saves image with resulting bounding boxes)


# Download image to disk for the given camera, return friendlier name
# TODO(Heath) use PIL or IO to keep in RAM, disk is going to be slow, though it
# still might be ok with the number of cameras we have as they're only updating
# their images roughly every minute - so it might not actually matter yet.
def download_image(url, cam_name):
  res = requests.get(url)
  if res.status_code != 200:
    print(res.status_code)
    return None
  #print(f"  Got image for {cam_name} at {url}...")
  image_name = f"{cam_name.lower().replace('/', '_')}.jpg"
  with open(f"images/{image_name}", 'wb') as f:
    f.write(res.content)
  return image_name

# Count instances of "vehicle_classes" predicted
def get_vehicle_count(model, scores, classes, vehicle_classes):
  vehicle_count = 0
  for score, class_idx in zip(scores, classes):
    class_label = model.get_label_for_idx(class_idx)
    # TODO (Heath): other labels that we want to count? (motorcyle, etc)
    if class_label in vehicle_classes:
      vehicle_count += 1
  return vehicle_count

# This is the main "service" - just loop indefinitely and grab traffic cam pics,
# YOLO them, and stick results in a database - currently thinking it could be
# completely standalone and hit an api to submit the data. Maybe overkill for
# MVP, TBD
def main():
  # Set up YOLO
  # TODO(Heath): these should be args
  model_dir = "model_data/"
  class_file = "model_data/coco_classes.txt"
  anchor_file = "model_data/yolo_anchors.txt"
  vehicle_classes = ["car", "truck"] # which classes to count
  input_size = (608, 608)
  yolo_model = YoloModel(model_dir, class_file, anchor_file, input_size)
  
  cameras = utils.get_cams_from_page()
  while True:
    # This whole step could be processed independently for each url
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for camera in cameras:
      label, url = camera["name"], camera["link"]
      # Get image from server
      # Also not sure whether we want to overwrite each time (as we are doing
      #  now) or save the images with a timestamp, or save the input image with
      # the bounding box predictions, tbd
      image_name = download_image(url, label)
      if image_name is None:
        continue

      # Run prediction
      tic = time.perf_counter()
      scores, boxes, classes = yolo_model.predict(image_name)
      print(f"  Prediction Time: {time.perf_counter() - tic} secs")

      # Parse and save results
      vehicles = get_vehicle_count(yolo_model, scores, classes, vehicle_classes)
      print(f"{label},{timestamp},{vehicles}")
      if SAVE_IMAGE:
        # Debug (save image with boxes)
        output_image = save_image_with_boxes(
          yolo_model.class_names, image_name, boxes, classes, scores)
    # Adjust to not run the same frame too many times, the pics only update
    # roughly every minute or so. With ~50 cams taking 0.5 secs each to
    # process, that's still only 25 seconds, so we can take a little break to
    # avoid too many duplicate runs
    time.sleep(20.0)



if __name__ == "__main__":
  main()