# RhodyCarCounter
Use Yolo to count the cars passing by traffic cams mostly in the Providence, RI area. 

## Backend
### Data and API
Uses Postgres database to store the data, and `FastAPI` with `sqlalchemy` to serve the data up for a public API. The API can be tested ([here](https://rhodycarcounter-production.up.railway.app/api/cameras) and [docs](https://rhodycarcounter-production.up.railway.app/docs/)).

### Car Detection Model
Mostly created to play around with the Yolo model implementation introduced
through a programming assignment in the Coursera Deep Learning course. Uses
the core implementation introduced there, but the interface to the model has
been modified a bit to make it easier to use in the service. It pulls all the
cam data from the PVD traffic site, runs Yolo on the images with some
pre-trained weights, and prints the results. The model does ok with car
detection using the pre-trained weights, but it was trained on a dash cam
footage, so it could be fine tuned to hopefully detect more of the cars in the
frame.

Sometimes it does a pretty good job:

![good_detections](/docs/img/6_10%20interchange.jpg "RT 6/10 near PVD mall")

And other times, not so much:

![bad_detections](/docs/img/sherman%20ave.jpg "The model finds a train")

Really, a train!? 

So we've got room to improve!

#### Most Recent Images
The worker sticks the cameras and the results of the car counting into the
database, and uploads the latest labelled image from a camera to s3.

For example, here's the most recently processed snapshot from the traffic camera at the Rt 6/10 interchange across from the Providence Place mall.

![Most recent RT 6/10 camera with labels](https://rhodycarcounter.s3.amazonaws.com/6_10+interchange.jpg)

Currently the worker is running on my personal desktop 🙃. So uptime is going
to be a little sketchy. I really just don't want to pay for cloud GPU time at the moment.

It runs through all the cameras every 5 minutes, but that might be adjusted after looking at the data more. And after determining how much data I can store for free 🤣.

### Model Improvement
I am planning to start to collect a small sample of images and label them
myself, especially some examples where the model preformed poorly, and retrain
just the last layer on the new data. It will also help to remove the classes
and only detect vehicles.

### Backend Directory Structure
The directories contain different parts of the project:
- `worker` - this is meant to run as a 'service', just loop for ever,
pull down images from the traffic cams, run YOLO on them, and drop the results into a postgres database.
- `database` - contains the database model, using SQLAlchemy as an ORM to make things easier
- `api.py` - contains the `FastAPI` app that connects to the database and exposes the path operations to get to the data (GET only).

NOTE(Heath): To get railway working, I had to remove tensorflow requirement
from the requirements.txt file. I couldn't figure out how to tell NIXPACKS to
use a special requirements.txt file and it can't install tensorflow, so I just
removed the requirement from the requirement.txt file (it's only used by the 
worker) - I kept it in the requirements-all.txt file.

## Frontend
WIP!
Going to use the API described above to show the data  
