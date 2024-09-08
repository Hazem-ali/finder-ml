# Use the Alpine-based Python 3.9 image
FROM python:3.9-alpine

# Install system dependencies required by face_recognition and other Python packages
RUN apk add --no-cache \
    build-base \
    cmake \
    git \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    musl-dev \
    mysql-client \
    mysql-dev

    
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1

    
EXPOSE 5000

CMD ["python", "main.py"]
