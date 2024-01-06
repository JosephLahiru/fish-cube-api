FROM python:3.10.0
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install --upgrade pip
WORKDIR /fish-cube-api
ADD . /fish-cube-api/
RUN sh download_models.sh
RUN pip install -r requirements.txt
CMD ["python", "app.py"]