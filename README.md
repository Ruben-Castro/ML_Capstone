# UCSD Machine Learning Capstone Project

## Overview 

This is my USCD ML Bootcamp capstone project it is a SaaS web application that allows its users to submit mp4 video files. It then allows the user to download an anotated video with the bounding boxes corresponding to persons in the video. The DL model used for object detection is YOLO V3.

#### production application: [production site](http://ruben-castro-ucsd-capstone.westus.azurecontainer.io/)


## Yolo v3 overview 
YOLOv3 (You Only Look Once, Version 3) is a real-time object detection algorithm that identifies specific objects in videos, live feeds, or images. YOLO uses features learned by a deep convolutional neural network to detect an object. Versions 1-3 of YOLO were created by Joseph Redmon and Ali Farhadi.

YOLO is a Convolutional Neural Network (CNN) for performing object detection in real-time. CNNs are classifier-based systems that can process input images as structured arrays of data and identify patterns between them. YOLO has the advantage of being much faster than other networks and still maintains accuracy.

It allows the model to look at the whole image at test time, so its predictions are informed by the global context in the image. YOLO and other convolutional neural network algorithms “score” regions based on their similarities to predefined classes.

High-scoring regions are noted as positive detections of whatever class they most closely identify with. For example, in a live feed of traffic, YOLO can be used to detect different kinds of vehicles depending on which regions of the video score highly in comparison to predefined classes of vehicles.

It is because of its balance of high acuracy and speed that we chose this model over other models in the object detection sphere for example Faster R-CNN which is very accurate but despite its name not very fast.


## Frontend 
The frontend project is a simple React SPA that uses Material UI, React Query, and Axios that allows users to upload one or multiple mp4 files at a time.

## Backend API 
The Backend API was built using FASTAPI for more infomation please visit their docs [fastAPI Documentation](https://fastapi.tiangolo.com/)


I also used azure blob store to store the user uploaded mp4 the processed avi file and a csv file containing the bounding boxes generated by yolov3

## Running The Project Local

####  1) install docker to your computer 

####  2) clone this repo 

####  3) modify Dockerfile inside api/ directory change all ENV variables to your corresponding azure blob storage connection string and containers

####  4) in the root directory type the following command in a terminal 

##### docker-compose -f docker-compose-dev.yml up
This will run the react application on localhost:3000 and the api with the yolov3 model on localhost



## Future state goals

- Including deepsort into our model. This will our ML model to keep track of each individual person and their direction. 
- Periodically retrain the model 

- Improve web application by adding the following 
    - Sign In 
    - payment system 
    - realtime/near realtime model outputs
    - api only interface so that users can stream live video directly to the api 
    - give users the ability to retrain their model and anotate their own data with bounding boxes for training 

- seperate the model from the api layer via a background task manager for example celery 
    


