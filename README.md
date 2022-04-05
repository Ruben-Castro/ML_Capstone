# UCSD Machine Learning Capstone Project

## Overview 

The Objective of this capstone project is to provide multi camera object detection. The goal is for our Machine Learning Model to detect people from multiple cameras accuractly given an input of video streams our output will be video frames anotated with a bounding box around the people in the video.



## Running Project Locally 

###  0) modify Dockerfile inside api/ directory change all ENV variables to your corresponding azure blob storage connection string and containers

###  1) install docker to your computer 

###  2) clone this repo 

###  3) in the root directory type the following command in a terminal 

#### docker-compose -f docker-compose-dev.yml up
This will run the react application on localhost:3000 and the api with the yolov3 model on localhost

