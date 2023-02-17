#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import scipy.io
import scipy.misc
import numpy as np
import pandas as pd
import PIL
from PIL import ImageFont, ImageDraw, Image
import tensorflow as tf
from tensorflow.python.framework.ops import EagerTensor

from tensorflow.keras.models import load_model
from yad2k.models.keras_yolo import yolo_head
from yad2k.utils.utils import draw_boxes, get_colors_for_classes, scale_boxes, read_classes, read_anchors, preprocess_image

class YoloModel:

    def __init__(self, model_dir, class_file, anchor_file, input_size):
        self.class_names = read_classes(class_file)
        self.anchors = read_anchors(anchor_file)
        self.input_size = input_size
        self.model = load_model(model_dir, compile=False)

    def yolo_filter_boxes(
        self, boxes, box_confidence, box_class_probs, threshold = .6):
        """Filters YOLO boxes by thresholding on object and class confidence.
        
        Arguments:
            boxes -- tensor of shape (19, 19, 5, 4)
            box_confidence -- tensor of shape (19, 19, 5, 1)
            box_class_probs -- tensor of shape (19, 19, 5, 80)
            threshold -- real value, if [ highest class probability score < threshold],
                        then get rid of the corresponding box

        Returns:
            scores -- tensor of shape (None,), containing the class probability score for selected boxes
            boxes -- tensor of shape (None, 4), containing (b_x, b_y, b_h, b_w) coordinates of selected boxes
            classes -- tensor of shape (None,), containing the index of the class detected by the selected boxes

        Note: "None" is here because you don't know the exact number of selected boxes, as it depends on the threshold. 
        For example, the actual output size of scores would be (10,) if there are 10 boxes.
        """
        
        ### START CODE HERE
        # Step 1: Compute box scores
        ##(≈ 1 line)
        box_scores = box_class_probs * box_confidence

        # Step 2: Find the box_classes using the max box_scores, keep track of the corresponding score
        ##(≈ 2 lines)
        # IMPORTANT: set axis to -1
        box_classes = tf.math.argmax(box_scores, axis=-1)
        box_class_scores = tf.math.reduce_max(box_scores, axis=-1)
        
        # Step 3: Create a filtering mask based on "box_class_scores" by using "threshold". The mask should have the
        # same dimension as box_class_scores, and be True for the boxes you want to keep (with probability >= threshold)
        ## (≈ 1 line)
        filtering_mask = box_class_scores >= threshold
        
        # Step 4: Apply the mask to box_class_scores, boxes and box_classes
        ## (≈ 3 lines)
        scores = tf.boolean_mask(box_class_scores, filtering_mask)
        boxes = tf.boolean_mask(boxes, filtering_mask)
        classes = tf.boolean_mask(box_classes, filtering_mask)
        ### END CODE HERE
        
        return scores, boxes, classes

    def yolo_non_max_suppression(
        self, scores, boxes, classes, max_boxes = 10, iou_threshold = 0.5):
        """
        Applies Non-max suppression (NMS) to set of boxes
        
        Arguments:
        scores -- tensor of shape (None,), output of yolo_filter_boxes()
        boxes -- tensor of shape (None, 4), output of yolo_filter_boxes() that have been scaled to the image size (see later)
        classes -- tensor of shape (None,), output of yolo_filter_boxes()
        max_boxes -- integer, maximum number of predicted boxes you'd like
        iou_threshold -- real value, "intersection over union" threshold used for NMS filtering
        
        Returns:
        scores -- tensor of shape (None, ), predicted score for each box
        boxes -- tensor of shape (None, 4), predicted box coordinates
        classes -- tensor of shape (None, ), predicted class for each box
        
        Note: The "None" dimension of the output tensors has obviously to be less than max_boxes. Note also that this
        function will transpose the shapes of scores, boxes, classes. This is made for convenience.
        """
        
        max_boxes_tensor = tf.Variable(max_boxes, dtype='int32')     # tensor to be used in tf.image.non_max_suppression()

        # Use tf.image.non_max_suppression() to get the list of indices corresponding to boxes you keep
        nms_indices = tf.image.non_max_suppression(
            boxes, scores, max_boxes_tensor)
        
        # Use tf.gather() to select only nms_indices from scores, boxes and classes
        scores = tf.gather(scores, nms_indices)
        boxes = tf.gather(boxes, nms_indices)
        classes = tf.gather(classes, nms_indices)
        return scores, boxes, classes


    def yolo_boxes_to_corners(self, box_xy, box_wh):
        """Convert YOLO box predictions to bounding box corners."""
        box_mins = box_xy - (box_wh / 2.)
        box_maxes = box_xy + (box_wh / 2.)

        return tf.keras.backend.concatenate([
            box_mins[..., 1:2],  # y_min
            box_mins[..., 0:1],  # x_min
            box_maxes[..., 1:2],  # y_max
            box_maxes[..., 0:1]  # x_max
        ])


    def yolo_eval(
        self, yolo_outputs, image_shape = (720, 1280), max_boxes=10, score_threshold=.6, iou_threshold=.5):
        """
        Converts the output of YOLO encoding (a lot of boxes) to your predicted boxes along with their scores, box coordinates and classes.
        
        Arguments:
        yolo_outputs -- output of the encoding model (for image_shape of (608, 608, 3)), contains 4 tensors:
                        box_xy: tensor of shape (None, 19, 19, 5, 2)
                        box_wh: tensor of shape (None, 19, 19, 5, 2)
                        box_confidence: tensor of shape (None, 19, 19, 5, 1)
                        box_class_probs: tensor of shape (None, 19, 19, 5, 80)
        image_shape -- tensor of shape (2,) containing the input shape, in this notebook we use (608., 608.) (has to be float32 dtype)
        max_boxes -- integer, maximum number of predicted boxes you'd like
        score_threshold -- real value, if [ highest class probability score < threshold], then get rid of the corresponding box
        iou_threshold -- real value, "intersection over union" threshold used for NMS filtering
        
        Returns:
        scores -- tensor of shape (None, ), predicted score for each box
        boxes -- tensor of shape (None, 4), predicted box coordinates
        classes -- tensor of shape (None,), predicted class for each box
        """
        
        # Retrieve outputs of the YOLO model (≈1 line)
        box_xy, box_wh, box_confidence, box_class_probs = yolo_outputs
        
        # Convert boxes to be ready for filtering functions (convert boxes box_xy and box_wh to corner coordinates)
        boxes = self.yolo_boxes_to_corners(box_xy, box_wh)
        
        # Use one of the functions you've implemented to perform Score-filtering with a threshold of score_threshold (≈1 line)
        scores, boxes, classes = self.yolo_filter_boxes(boxes, box_confidence, box_class_probs, score_threshold)

        # Scale boxes back to original image shape.
        boxes = scale_boxes(boxes, image_shape)
        
        # Use one of the functions you've implemented to perform Non-max suppression with 
        # maximum number of boxes set to max_boxes and a threshold of iou_threshold 
        scores, boxes, classes = self.yolo_non_max_suppression(
            scores, boxes, classes, max_boxes, iou_threshold)
        return scores, boxes, classes

    def get_label_for_idx(self, idx):
        return self.class_names[idx]

    def predict(self, image_file):
        """
        Runs the graph to predict boxes for "image_file". Prints and plots the predictions.
        
        Arguments:
        image_file -- name of an image stored in the "images" folder.
        
        Returns:
        out_scores -- tensor of shape (None, ), scores of the predicted boxes
        out_boxes -- tensor of shape (None, 4), coordinates of the predicted boxes
        out_classes -- tensor of shape (None, ), class index of the predicted boxes
        
        Note: "None" actually represents the number of predicted boxes, it varies between 0 and max_boxes. 
        """

        # Preprocess your image
        image, image_data = preprocess_image(
            "images/" + image_file, model_image_size = (608, 608))
        yolo_model_outputs = self.model(image_data)
        yolo_outputs = yolo_head(
            yolo_model_outputs, self.anchors, len(self.class_names))
        out_scores, out_boxes, out_classes = self.yolo_eval(
            yolo_outputs, [image.size[1],  image.size[0]], 10, 0.3, 0.5)
        return out_scores, out_boxes, out_classes

def save_image_with_boxes(class_names, input_image, boxes, classes, scores):
    colors = get_colors_for_classes(len(class_names))
    image, image_data = preprocess_image(
        "images/" + input_image, model_image_size = (608, 608))
    draw_boxes(image, boxes, classes, class_names, scores)
    image.save(os.path.join("out", input_image), quality=100)
    return image

def main():
    # Example usage:
    model_dir = "model_data/"
    class_file = "model_data/coco_classes.txt"
    anchor_file = "model_data/yolo_anchors.txt"
    input_size = (608, 608)
    yolo_model = YoloModel(model_dir, class_file, anchor_file, input_size)
    yolo_model.model.summary()

    input_image = "test.jpg"

    # predict
    scores, boxes, classes = yolo_model.predict(input_image)
    print(f'Found {len(boxes)} boxes for {"images/" + input_image}')
    
    # display some results:
    output_image = save_image_with_boxes(
        yolo_model.class_names, input_image, boxes, classes, scores)
    output_image = Image.open(os.path.join("out", input_image))
    plt.imshow(output_image)
    for score, box, class_idx in zip(scores, boxes, classes):
        label = yolo_model.get_label_for_idx(class_idx)
        print(label, float(score), np.array(box))
    plt.show()

if __name__ == "__main__":
    main()


# References
# This implementation was part of coursera deeplearning.ai course 4 homework
#
# The ideas presented in this notebook came primarily from the two YOLO papers. The implementation here also took significant inspiration and used many components from Allan Zelener's GitHub repository. The pre-trained weights used in this exercise came from the official YOLO website. 
# - Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi - [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640) (2015)
# - Joseph Redmon, Ali Farhadi - [YOLO9000: Better, Faster, Stronger](https://arxiv.org/abs/1612.08242) (2016)
# - Allan Zelener - [YAD2K: Yet Another Darknet 2 Keras](https://github.com/allanzelener/YAD2K)
# - The official YOLO website (https://pjreddie.com/darknet/yolo/) 
# 
# ### Car detection dataset
# 
# <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">The Drive.ai Sample Dataset</span> (provided by drive.ai) is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>. Thanks to Brody Huval, Chih Hu and Rahul Patel for  providing this data. 