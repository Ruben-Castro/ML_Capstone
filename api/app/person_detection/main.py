import argparse 
import sys 
import os.path 
import cv2 as cv 
import numpy as np 
from azure.storage.blob import ContentSettings
from app.azure import upload_to_csv_container, upload_to_processed_container

# Initialize the parameters
confThreshold = 0.5  #Confidence threshold
nmsThreshold = 0.4   #Non-maximum suppression threshold
inpWidth = 416       #Width of network's input image
inpHeight = 416      #Height of network's input image

PROCESSED_VIDEOS_PATH = '/code/app/processed_videos/'
CSVS_PATH='/code/app/csv_outputs/'
COCO_NAMES = "/code/app/person_detection/coco.names"
YOLO_CFG="/code/app/person_detection/yolov3.cfg"
YOLO_WEIGHTS="/code/app/person_detection/yolov3.weights"

def person_detection(video_file, device):
    classes = load_classes(COCO_NAMES, ['person'])
    net = configure_model(device,YOLO_CFG,YOLO_WEIGHTS)


    outputFile = "yolo_out_py.avi"
    csv_output = "yolo_out.csv"

    if (video_file):
        # Open the video file
        print("video_file:", video_file)
        if not os.path.isfile(video_file):
            print("Input video file ", video_file, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(video_file)

        actual_file_name =video_file.split('/')[4]
        print("actual_file_name ", actual_file_name)

        outputFile = PROCESSED_VIDEOS_PATH+actual_file_name.split('.')[0]+'_yolo_out.avi'
        csv_output = CSVS_PATH+actual_file_name.split('.')[0]+ "_yolo_out.csv"
       
  
    # Get the video writer initialized to save the output video
    vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

    frame_count = 0
    while cv.waitKey(1) < 0:
        
        # get frame from the video
        hasFrame, frame = cap.read()
    
        
        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            print("Output file is stored as ", outputFile)
            cap.release()
            #save to file
            processed_file_name = actual_file_name.split('.')[0]+'_yolo_out.avi'
            print(processed_file_name)
            upload_to_processed_container(processed_file_name) 
            csv_file_name = actual_file_name.split('.')[0]+"_yolo_out.csv"
            print(csv_file_name)
            upload_to_csv_container(csv_file_name)
            return outputFile
            break
        
        frame_count +=1 
        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(get_output_names(net))

        # Remove the bounding boxes with low confidence
        post_process(classes, frame, outs, frame_count,csv_output)

        # Write the frame with the detection boxes
        vid_writer.write(frame.astype(np.uint8))




def configure_model(device,model_configuration, model_weights):
    net = cv.dnn.readNetFromDarknet(model_configuration, model_weights)

    if(device =='cpu'):
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    elif(device == 'gpu'):
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

    return net

def get_output_names(net):

    #names of all layers in network
    layer_names = net.getLayerNames()

    #get the names of the layers with unconnected outputs
    return [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def draw_bounding_box(classes:list, frame, class_id:int, conf:str, left, top, right, bottom):
    if classes:
        if class_id < len(classes):
            label = '%.2f' %  conf
            cv.rectangle(frame, (left, top), (right, bottom), (255,178,50), 3)
            label = '{}:{}'.format(classes[class_id], label)

   

            #display the labelat the top of bounding box
            label_size, base_line = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            top = max(top, label_size[1])
            cv.rectangle(frame, (left, top - round(1.5*label_size[1])), (left + round(1.5*label_size[0]), top + base_line), (255, 255, 255), cv.FILLED)
            cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 1)

'''
Remove the bounding boxes that have a low confidence using non-maxima suppression 
'''
def post_process(classes, frame, outs, frame_count, csv_output):
    frame_height, frame_width = frame.shape[0], frame.shape[1]

    #go through all of the bounding boxes output from the network. Eliminate the ones with low confidence scores 
    #assign label as the class with the highest score 

    class_ids = []
    confidences = []
    boxes = []

    for out in outs: 
         for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > confThreshold:
                center_x = int(detection[0] * frame_width)
                center_y = int(detection[1] * frame_height)
                width = int(detection[2]* frame_height)
                height = int(detection[3] * frame_height)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    #preform non maximum suppression to eliminate overlaping bounding boxe 
   
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        draw_bounding_box(classes,frame, class_ids[i], confidences[i], left, top, left + width, top + height)
         
         #just like virat bounding box
        #write to file_instead
        with open(csv_output, 'a') as csv_file:
            csv_file.write("{}, {}, {}, {} \n".format(left, top, width, height))

'''Loads the coco classes limit them to person'''
def load_classes(class_file: str, class_filter:list) -> list:
    classes = None 
    with open(class_file, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')
    
    if classes == None:
        raise Exception("The file contanined no classes")

    if class_filter:
        for c in class_filter:
            if c not in classes:
                raise Exception("Class in class_filter is not a valid coco dataset class")

        return class_filter
    
    return classes 



