#!/usr/bin/env python3

import os
import sys
import numpy as np
import requests
from flask import Flask, request, jsonify, make_response, render_template
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from detect import run

# try:
#     os.system(
#         'python3 -m gdown.cli https://drive.google.com/uc?id=140nWkufV4fjzb18Bs910KQldIcUeVwMc -O modelss/')
#     os.system(
#         'python3 -m gdown.cli https://drive.google.com/uc?id=1XP-jlvvDaFwaRDNIuJGF1ZzieSoNHzp_ -O modelss/')
#     os.system(
#         'python3 -m gdown.cli https://drive.google.com/uc?id=1hTbFKPYOlSa13ew-hvxjVoXLbLqsbuYD -O modelss/')
# except Exception as e:
#     print(e)

app = Flask(__name__)

try:
    fish_type_model = load_model(
        'modelss/fish_type_model.h5')
    healty_unhealthy_yellowfin_model = load_model(
        'modelss/yellowfin_model.h5')
    healty_unhealthy_skipjack_model = load_model(
        'modelss/skipjack_model.h5')
except Exception as e:
    print(e)
    sys.exit(0)

fish_type_classes = ['Yellofin_tuna', 'Skipjack_tuna', "Invalid_image"]
healty_unhealthy_classes = ['Healthy', 'Unhealthy']

img_path = 'test_images/temp_image.jpg'


def add_headers(output):
    response = make_response(jsonify(output))
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


def download_image(url, save_path):
    with open(save_path, "wb") as f:
        response = requests.get(url)
        f.write(response.content)


def prepare(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = x / 255
    return np.expand_dims(x, axis=0)


def detect_fish_type(img_url):

    download_image(img_url, img_path)
    results = run(weights='modelss/best_11.pt', source=img_path)
    if(len(results)>0 and float(results[0][1])>0.9):
        img_data = prepare(img_path)
        result_vgg16 = fish_type_model.predict(img_data)
        print(result_vgg16)
        class_result = np.argmax(result_vgg16, axis=1)
        prediction = fish_type_classes[class_result[0]]

        return [prediction, img_data]
    else:
        os.remove(img_path)
        return([fish_type_classes[2],"n/a"])


def detect_healty_unhealthy(fish_type, img_data):

    model = healty_unhealthy_skipjack_model
    if (fish_type == fish_type_classes[0]):
        # select the yellofin model
        model = healty_unhealthy_yellowfin_model

    result_vgg16 = model.predict(img_data)
    class_result = np.argmax(result_vgg16, axis=1)
    prediction = healty_unhealthy_classes[class_result[0]]

    return [prediction, fish_type]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:

        fish_type_data = detect_fish_type(request.json['img_url'])

        if (fish_type_data[0] == fish_type_classes[2]):
            return add_headers({'prediction': "n/a", 'fish_type': "unknown"})
        else:
            try:
                prediction = detect_healty_unhealthy(
                    fish_type_data[0], fish_type_data[1])
                os.remove(img_path)
                return add_headers({'prediction': prediction[0], 'fish_type': prediction[1]})
            except Exception as _e:
                return add_headers({'prediction_error': str(_e)})
    except Exception as _e:
        return add_headers({'error': str(_e)})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=5)
