# RhodyCarCounter
Use Yolo to count the cars passing by traffic cams mostly in the Providence, RI area. 

## Overall Current Architecture
![Current Architecture](/docs/img/traffic_app_setup.png "Current Architecture")

## Backend
### Data and API
Uses Postgres database to store the data, and `FastAPI` with `sqlalchemy` to serve the data up for a public API. The API can be tested ([here](https://rhodycarcounter-production.up.railway.app/api/cameras) and [docs](https://rhodycarcounter-production.up.railway.app/docs/)).

### Car Detection Model
Originally created to play around with the Yolo model implementation introduced
through a programming assignment in the deeplearning.ai [Deep Learning courses](https://www.deeplearning.ai/courses/deep-learning-specialization/) on Coursera. Uses the YOLOv8 pretrained model from [ultralytics](https://docs.ultralytics.com/). I then trained it a little bit on some of the traffic cam data that is publically available a this [paper](https://proceedings.neurips.cc/paper/2019/file/ee389847678a3a9d1ce9e4ca69200d06-Paper.pdf), but we have a lot of room to improve. It pulls all the
cam data from the PVD traffic site.

#### Most Recent Images
The worker sticks the cameras and the results of the car counting into the
database, and uploads the latest labelled image from a camera to s3.

For example, here's the most recently processed snapshot from the traffic camera at the Rt 6/10 interchange across from the Providence Place mall.

![Most recent RT 6/10 camera with labels](https://rhodycarcounter.s3.amazonaws.com/6_10+interchange.jpg?)

The worker runs through all the cameras every 5 minutes, but that might be adjusted after looking at the data more. And after determining how much data I can store for free-ish 🤣.

### Model Improvement
I am planning to start to collect a small sample of images and label them
myself, especially some examples where the model preformed poorly, and retrain
just the last layer on the new data. It will also help to remove the classes
and only detect vehicles.

### Backend Directory Structure
The directories contain different parts of the project:
- `worker` - this is meant to run as a 'service', just loop for ever,
pull down images from the traffic cams, run YOLO on them, and drop the results into a postgres database.
- `api` - contains the `FastAPI` app that connects to the database and exposes the path operations to get to the data (GET only).

Both of these use the `database` module to connect to the database. It's
literally just duplicated in both places (I know...it was a hack to get railway to work).
I'm going to make it a submodule.

## Frontend
It's a work in progress (https://heathhenley.github.io/RhodyCarCounter/)

Using react, react-bootstrap, and react-leaftlet to create a map of the cameras
and the counts and show a table of all the available cameras. Uses recharts to
plot the latests data.