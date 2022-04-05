import os
import logging
from azure.storage.blob import BlobServiceClient, ContainerClient, __version__, ContentSettings
logger = logging.getLogger(__name__) 

CONNECT_STR = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.getenv('UPLOAD_CONTAINER_NAME')
PROCESSED_CONTAINER = os.getenv('PROCESSED_CONTAINER')
CSV_CONTAINER= os.getenv('CSVS_CONTAINER')


def __upload_to_container(container_name, file_location, file_name, content_settings):
    try:
        print("uploadinig file to azure")
        print("container_name: ", container_name)
        print("blob name: ", file_name)
        
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        with open(file_location+file_name, 'rb') as data:
            blob_client.upload_blob(data,overwrite=True, content_settings=content_settings)
    except Exception as ex:
        print("azure blob storage failed with the following exception")
        print("Exception:")
        print(ex)
        
def __delete_file(file_location, file_name):
    if os.path.exists(file_location+file_name):
        os.remove(file_location+file_name)
    else:
        logger.info("The file does not exist")

def upload_to_upload_container(file_name):
    file_location ="/code/app/uploaded_files/"
    my_content_settings = ContentSettings(content_type='video/mp4')
    __upload_to_container(CONTAINER_NAME,file_location, file_name, my_content_settings)
   


def upload_to_csv_container(file_name):
    file_location ="/code/app/csv_outputs/"
    my_content_settings = ContentSettings(content_type='text/csv')
    __upload_to_container(CSV_CONTAINER,file_location, file_name, my_content_settings)
    __delete_file(file_location, file_name)
    file_location ="/code/app/uploaded_files/"
    __delete_file(file_location, file_name)

def upload_to_processed_container(file_name):
    file_location="/code/app/processed_videos/"
    my_content_settings = ContentSettings(content_type='video/x-msvideo')
    __upload_to_container(PROCESSED_CONTAINER, file_location, file_name, my_content_settings)
    __delete_file(file_location, file_name)

def get_blobs_from_container(container_name):
    try:
        container_client = ContainerClient.from_connection_string(CONNECT_STR, container_name)
        blob_list = container_client.list_blobs()

        if blob_list:
            processed_files = [ {'filename':blob.name, 'uploaded':blob.creation_time, 'content-type':blob.content_settings.content_type} for blob in blob_list]
            return {'files': processed_files }
    
    except Exception as ex:
        print("azure blob storage failed with the following exception")
        print("Exception:")
        print(ex)
     
    #nothing is stored in the container
    return {'files': [] }

def get_blob_from_container(container_name, blob_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        return blob_client.download_blob().chunks()
 

    except Exception as ex:
        logger.info("azure blob storage failed with the following exception")
        logger.info("Exception:")
        logger.info(ex)


