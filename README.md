# RhodyCarCounter
Use Yolo to count the cars passing by traffic cams mostly in the Providence, RI area. 

## Overall Current Architecture
![Current Architecture](/docs/img/traffic_app_setup.png "Current Architecture")

## Backend
### Data and API
Uses Postgres database to store the data, and `FastAPI` with `sqlalchemy` to serve the data up for a public API. The API can be tested ([here](https://rhodycarcounter-production.up.railway.app/api/cameras) and [docs](https://rhodycarcounter-production.up.railway.app/docs/)).

### Car Detection Model
Originally created to play around with the Yolo model implementation introduced
through a programming assignment in the deeplearning.ai [Deep Learning courses](https://www.deeplearning.ai/courses/deep-learning-specialization/) on Coursera. Uses the YOLOv8 pretrained model from [ultralytics](https://docs.ultralytics.com/). I then trained it a little bit on some of the traffic cam data that is publically available and was used for this [paper](https://proceedings.neurips.cc/paper/2019/file/ee389847678a3a9d1ce9e4ca69200d06-Paper.pdf). But we have a lot of room to improve. It pulls all the camera images directly from the [RIDOT](https://www.dot.ri.gov/travel/index.php) traffic site.

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

## How to run locally
### The whole system
I just added a docker-compose file to run the backend and the frontend locally. You can run it with: `docker compose up` and it will spin up the API server on 
http://localhost:5001, a postgres database on port 5432, and the frontend on http://localhost:3000/RhodyCarCounter. It also copies the cameras from the the camera table in the "production" database. 

The last thing to do is to point the front end to the API running on your local machine at http://localhost:5001/api. It should be simple to set up, but I haven't set it up yet. So right now even if you run the frontend locally,, it will still pull data from the production API.

### Individual parts
If you only want to run the frontend:

- clone repo
- navigate to the frontend/traffic_count directory
- run npm install - to install the dependencies
- run npm start - the start the dev server on localhost

Running the backend will require a little more work. 

In general the idea is:
- set the environment variables that are in this template: https://github.com/heathhenley/RhodyCarCounter/blob/main/backend/env-template.bat (you don't actually need the AWS ones unless you want to stick the images in an AWS bucket) --> the backend needs a database, I'm running postgres on railway.app, you could install locally or even use sqlite. The DB_CONNECT_STR for sqlite should be something like "file:./db.sqlite" which is simpler than postgres.
- clone the repo and navigate to backend/api
to run the api: (you need python 3.10 or higher)
- create a venv to install the api dependencies python -m venv api_env and activate it (run Scripts/activate)
- install the api dependencies with python -m pip install -r requirements-api.txt
- run the api with uvicorn api:app --reload
it uses FastAPI, and their docs are awesome (https://fastapi.tiangolo.com/)

If you want to run the worker, I would create a separate virtual environment:
- create a venv to install the api dependencies python -m venv worker_env and activate it (run Scripts/activate)
- install the worker dependencies with python -m pip install -r requirements-worker.txt
- run the worker with python worker/traffic.py
