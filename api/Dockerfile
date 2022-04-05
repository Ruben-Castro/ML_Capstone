FROM continuumio/anaconda3
FROM opencvcourses/opencv-docker

WORKDIR /code


ENV AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=trainingdataimages;AccountKey=69ULOHEnqyVRRqs/uqsTkCm59Wi4J62p1q7RbmOh72WeYg7PdfAFNAEv5piBpSXuow0sgld1mJG9OE+j79Hiug==;EndpointSuffix=core.windows.net"
ENV UPLOAD_CONTAINER_NAME="video-uploads"
ENV PROCESSED_CONTAINER="processed-videos"
ENV CSVS_CONTAINER="bounding-boxes-csvs"

COPY ./requirements.txt /code/requirements.txt

RUN  pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]