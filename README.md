# RhodyCarCounter
Use Yolo to count the cars passing by traffic cams mostly in the Providence, RI area

Mostly created to play around with the Yolo model implementation introduced through
a programming assignment in the Coursera Deep Learning course. Uses the core
implementation introduced there, but the interface to the model has been modified
a bit to make it easier to use in the service. It pulls all the cam data from the
PVD traffic site, runs Yolo on the images with some pre-trained weights, and
prints the results. The model does ok with car detection using the pretrained
weights, but it was trained on a dash cam footage, so it could be fine tuned to
hopefully detect more of the cars in the frame.  I'm planning to manually label
some of the data from these cams, and also search for traffic cam labelled datasets
that could be used. After fine tuning, the images and stats will be stored in a
database, and a viewer can be added to show the datastreams. 
