FROM python

WORKDIR /myapp

COPY . /myapp

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

CMD ["fastapi", "dev", "main.py"]
