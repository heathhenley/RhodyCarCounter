# RhodyCarCounter
Use Yolo to count the cars passing by traffic cams mostly in the Providence, RI area

Mostly created to play around with the Yolo model implementation introduced through
a programming assignment in the Coursera Deep Learning course. Uses the core
implementation introduced there, but the interface to the model has been modified
a bit to make it easier to use in the service. It pulls all the cam data from the
PVD traffic site, runs Yolo on the images with some pre-trained weights, and
prints the results. The model does ok with car detection using the pretrained
weights, but it was trained on a dash cam footage, so it could be fine tuned to
hopefully detect more of the cars in the frame. The worker sticks the cameras and the results of the car counting into a postgres database running railway. The data is made available via API using FastAPI. 

The directories contain different parts of the project:
- `worker` - this is meant to run as a 'service', just loop for ever,
pull down images from the traffic cams, run YOLO on them, and drop the results into a postgres database.
- `database` - contains the database model, using SQLAlchemy as an ORM to make things easier
- `api.py` - contains the `FastAPI` app that connects to the database and exposes the path operations to get to the data (GET only).

NOTE(Heath): hacked to get railway working - I couldn't figure out how to tell NIXPACKS to use a special requirements.txt file and it can't install tensorflow, so I just removed the requirement from the requirement.txt file - I kept it in the requirements-all.txt file. 

API can be tested [here](https://rhodycarcounter-production.up.railway.app/api/cameras) for example, and [docs](https://rhodycarcounter-production.up.railway.app/docs/). 
