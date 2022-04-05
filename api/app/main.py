from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
import os, uuid
from azure.storage.blob import BlobServiceClient, ContainerClient, __version__,ContentSettings
from fastapi.middleware.cors import CORSMiddleware
from app.person_detection.main import person_detection
from app.azure import upload_to_upload_container, get_blobs_from_container, get_blob_from_container
import shutil
import logging
from starlette.responses import FileResponse 
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__) 


CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('UPLOAD_CONTAINER_NAME')
PROCESSED_CONTAINER = os.getenv('PROCESSED_CONTAINER')
CSV_CONTAINER= os.getenv('CSVS_CONTAINER')



app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#create a subprocess that runs yolo-v3
def process_video(file):
    logger.info("Process Video Triggered")
    output_files = person_detection(file, 'cpu')



#saves file to server
def save_to_server(file, file_name):
    logger.info("saving file toserver")
    output_file = "/code/app/uploaded_files/"+str(file.filename)
    with open(output_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)   



'''
Add videos to azure_blob_storage works
'''
@app.post("/uploadvideos")
async def upload_videos( background_tasks: BackgroundTasks, files: List[UploadFile]=File(...)):
    logger.info("inside upload_videos")
    valid_files = []
    
    #check if files are 
    for file in files:
        if file.content_type == "video/mp4":
            valid_files.append(file)
           
            #save file to our server do this synchronoushly so that the background tasks work.
            save_to_server(file, file.filename)
            
            #upload files to azure-blob-storage
            background_tasks.add_task(upload_to_upload_container, file.filename)
           
            #process video in the background should use celery and rabbit mq in the future
            background_tasks.add_task(process_video,"/code/app/uploaded_files/"+file.filename)
           
    #return the filenames of the files added to azure-blob-storage
    return {"filenames": [file.filename for file in valid_files]}


'''
get list of files uploaded and creation times
''' 
@app.get("/videos")
async def get_videos():
    data = get_blobs_from_container(PROCESSED_CONTAINER)
    return data

    

'''
Returns list of all of the processed videos including url to donwload them from azure 
'''
@app.get('/videos/{file_name}')    
async def get_processed_videos(file_name):
    return StreamingResponse(get_blob_from_container(PROCESSED_CONTAINER,file_name),media_type="video/x-msvideo")
    
     
    
''' 
get the csvdata for a processed video from azure container including link to download it from azure 
''' 
@app.get("/csvdata/{file_name}")
async def get_csvdata(file_name):
   return StreamingResponse(get_blob_from_container(CSV_CONTAINER,file_name),media_type="text/csv")