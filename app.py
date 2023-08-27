import os
import numpy as np
import requests
from flask import Flask, request, jsonify, make_response, render_template
from keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

try:
    fish_type_model = load_model(
        'models/detecting_freshness_of_fish_cube_VGG16.h5')
    healty_unhealthy_yellowfin_model = load_model(
        'models/detecting_freshness_of_fish_cube_VGG16.h5')
    healty_unhealthy_skipjack_model = load_model(
        'models/detecting_freshness_of_fish_cube_VGG16.h5')
except Exception as e:
    print(e)
    exit(0)

fish_type_classes = ['Yellofin_tuna', 'Skipjack_tuna', "Invalid_image"]
healty_unhealthy_classes = ['Healthy', 'Unhealthy']

img_path = 'temp/temp_image.jpg'


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
    img_data = prepare(img_path)
    result_vgg16 = fish_type_model.predict(img_data)
    class_result = np.argmax(result_vgg16, axis=1)
    prediction = fish_type_classes[class_result[0]]

    return [prediction, img_data]


def detect_healty_unhealthy(fish_type, img_data):

    model = healty_unhealthy_skipjack_model
    if (fish_type == fish_type_classes[0]):
        # select the yellofin model
        model = healty_unhealthy_yellowfin_model

    result_vgg16 = model.predict(img_data)
    class_result = np.argmax(result_vgg16, axis=1)
    prediction = healty_unhealthy_classes[class_result[0]]

    return prediction


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        fish_type_data = detect_fish_type(request.json['img_url'])

        if (fish_type_data[0] == fish_type_classes[2]):
            return add_headers({'error': fish_type_data[0]})
        else:
            try:
                prediction = detect_healty_unhealthy(
                    fish_type_data[0], fish_type_data[1])
                os.remove(img_path)
                return add_headers({'prediction': prediction})
            except Exception as _e:
                return add_headers({'error': str(_e)})
    except Exception as _e:
        return add_headers({'error': str(_e)})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=5)
