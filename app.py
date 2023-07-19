import os
import numpy as np
import requests
from flask import Flask, request, jsonify, make_response
from keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

model_vgg16 = load_model('models/detecting_freshness_of_fish_cube_VGG16.h5')
classes = ['Healthy', 'Unhealthy']


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


@app.route('/predict', methods=['POST'])
def predict():
    try:
        img_url = request.json['img_url']
        img_path = 'temp/temp_image.jpg'
        download_image(img_url, img_path)
        img_data = prepare(img_path)
        result_vgg16 = model_vgg16.predict(img_data)
        class_result = np.argmax(result_vgg16, axis=1)
        prediction = classes[class_result[0]]
        os.remove(img_path)
        return add_headers({'prediction': prediction})
    except Exception as e:
        return add_headers({'error': str(e)})


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000, threads=5)
