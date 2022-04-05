# UCSD Machine Learning Capstone Project

## Overview 

The Objective of this capstone project is to provide multi camera object detection. The goal is for our Machine Learning Model to detect people from multiple cameras accuractly given an input of video streams our output will be video frames anotated with a bounding box around the people in the video.



## Training Data 


### 3dpes_data 

website: https://aimagelab.ing.unimore.it/imagelab/page.asp?IdPage=16

D. Baltieri; R. Vezzani; R. Cucchiara "3DPes: 3D People Dataset for Surveillance and Forensics" Proceedings of the 2011 joint ACM workshop on Human gesture and behavior understanding, vol. 1, Scottsdale, Arizona, USA, pp. 59 -64 , Nov 28 - Dec 1 2011, 2011

### meva_dataset

website: https://mevadata.org/


### virat_dataset Release 2.0

website: https://viratdata.org/

"A Large-scale Benchmark Dataset for Event Recognition in Surveillance Video" by Sangmin Oh, Anthony Hoogs, Amitha Perera, Naresh Cuntoor, Chia-Chih Chen, Jong Taek Lee, Saurajit Mukherjee, J.K. Aggarwal, Hyungtae Lee, Larry Davis, Eran Swears, Xiaoyang Wang, Qiang Ji, Kishore Reddy, Mubarak Shah, Carl Vondrick, Hamed Pirsiavash, Deva Ramanan, Jenny Yuen, Antonio Torralba, Bi Song, Anesco Fong, Amit Roy-Chowdhury, and Mita Desai, in Proceedings of IEEE Comptuer Vision and Pattern Recognition (CVPR), 2011."


### Virat Parser 
 Python CLI application that takes in the folder paths for virat original videos, virat anotations and target folder - the location where we want the videos with bounding boxes to be stored. 



 ### Yolo V3 
 Yolo v3 is used as the object detection alogrithm for this application. I'm initially using the default application configuration. with the provided weights. 


 ### Deepsort 
Deepsort is used for object tracking implementation provided by: "REFRENCE author" "REFRENCE RESEARCH PAPER"