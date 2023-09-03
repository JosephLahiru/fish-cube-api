FROM python:3.10.0-alpine
RUN pip install --upgrade pip
WORKDIR /fish-cube-api
ADD . /fish-cube-api/
RUN sh download_models.sh
RUN pip install -r requirements.txt
CMD ["python", "app.py"]