FROM continuumio/anaconda3
FROM opencvcourses/opencv-docker

WORKDIR /code


ENV AZURE_STORAGE_CONNECTION_STRING="YOUR_CONNECTION_STRING"
ENV UPLOAD_CONTAINER_NAME="video-uploads"
ENV PROCESSED_CONTAINER="processed-videos"
ENV CSVS_CONTAINER="bounding-boxes-csvs"

COPY ./requirements.txt /code/requirements.txt

RUN  pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]