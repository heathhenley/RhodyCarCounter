import datetime
import requests
import time
from yolo import YoloModel, save_image_with_boxes

SAVE_IMAGE = True # debug (saves image with resulting bounding boxes)

# TODO(Heath): parse this from page html - in case cams are ever added or
# removed from the list
URLS = {
  'Boadway': 'https://www.dot.ri.gov/img/travel/camimages/95_37.0_S_CAM%20-%20Broadway%20(Prov).jpg',
  'Exit 33 (Route 10)': 'https://www.dot.ri.gov/img/travel/camimages/95_33.6_S_CAM%20-%20Rt%2010.jpg',
  'Elmwood Ave' : 'https://www.dot.ri.gov/img/travel/camimages/95_34.0_S_CAM%20-%20Elmwood%20Ave.jpg'
  }

# Set up yolo
#   Grab image from server
#   Run yolo
#   Compute stats
#   Produce stats (just going to log for now)

def download_image(url, cam_name):
  res = requests.get(url)
  if res.status_code != 200:
    print(res.status_code)
    return None
  print(f"  Got image for {cam_name} at {url}...")
  image_name = f"{cam_name.lower()}.jpg"
  with open(f"images/{image_name}", 'wb') as f:
    f.write(res.content)
  return image_name

def main():
  # Set up YOLO
  # TODO(Heath): these should be args
  model_dir = "model_data/"
  class_file = "model_data/coco_classes.txt"
  anchor_file = "model_data/yolo_anchors.txt"
  input_size = (608, 608)
  yolo_model = YoloModel(model_dir, class_file, anchor_file, input_size)
  
  while True:
    # This whole step could be processed independently for each url
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for label, url in URLS.items():
      # Get image from server
      # TODO(Heath): this is not efficient, saves the image to disk and then
      # eventually reads it back in, could just keep in memory.
      # Also not sure whether we want to overwrite each time (as we are doing
      #  now) or save the images with a timestamp
      image_name = download_image(url, label)
      if image_name is None:
        continue
      # Run prediction
      tic = time.perf_counter()
      scores, boxes, classes = yolo_model.predict(image_name)
      print(f"  Prediction Time: {time.perf_counter() - tic} secs")

      # Log results (eventually produce or save)
      car_count = 0
      for score, class_idx in zip(scores, classes):
        class_label = yolo_model.get_label_for_idx(class_idx)
        # TODO (Heath): other labels that we want to count? (motorcyle, etc)
        if class_label == 'car' or class_label != "truck":
          car_count += 1
      print(f"Cam: {label}, Time: {timestamp}, Traffic: {car_count} vehicles")
      if SAVE_IMAGE:
        # Debug (save image with boxes)
        output_image = save_image_with_boxes(
          yolo_model.class_names, image_name, boxes, classes, scores)
    time.sleep(10.0) # Adjust (pics only updated on every minute or so...)



if __name__ == "__main__":
  main()