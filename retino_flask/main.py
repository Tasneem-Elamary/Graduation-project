from flask import Flask
from flask import request
from flask import jsonify
from PIL import Image
import cloudinary
from imageio import imread
import cloudinary.uploader
import numpy as np
import pandas as pd
import tensorflow as tf
import cv2

from resnet.preprossing import preprocess_image
from unet.test_ex import predict_ex
from unet.test_ma import predict_ma
from unet.test_he import predict_he
from unet.test_se import predict_se

# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# from tensorflow.keras.models import load_model
# from tensorflow.python.keras.backend import set_session
# #tf_config = some_custom_config
# sess = tf.compat.v1.Session()
# graph = tf.compat.v1.get_default_graph()
# set_session(sess)


print(tf.__version__)
resnetmodel = tf.keras.models.load_model("resnet/80_accuracy.h5")
grades = {0: "No DR", 1: "Mild", 2: "Moderate", 3: "Severe", 4: "proliferative"}

cloudinary.config(
    cloud_name="dfvv2i9vk",
    api_key="971697155345565",
    api_secret="ZSWT_CzGbqnuoFErIgvt0BY0PDg",
)

app = Flask(__name__)


@app.route("/grade", methods=["POST"])
def grade():
    # tf.compat.v1.enable_eager_execution()
    message = request.get_json(force=True)
    image_url = message["originalimage"]
    print(image_url)
    input_img = preprocess_image(image_url)
    input_img = np.expand_dims(input_img, axis=0)
    input_img = (1.0 / 255) * (input_img)
    print(input_img.shape)
    # global sess
    # global graph
    # with graph.as_default():
    #     set_session(sess)
    #     predicted_label = resnetmodel.predict(input_img)
    predicted_label = resnetmodel.predict(input_img)
    predicted_label = np.argmax(predicted_label)
    predicted_label = grades[predicted_label]
    print(predicted_label)
    response = {"grade": predicted_label}
    # print(response['grade'])
    return jsonify(response)


@app.route("/hardExudates", methods=["POST"])
def hardExudates():
    # tf.compat.v1.disable_eager_execution()
    message = request.get_json(force=True)
    image_url = message["originalimage"]
    identifier = message["identifier"]
    # input_img = imread(image_url)
    out_img = predict_ex(image_url)
    out_img.save("ex.png")

    upload_result = cloudinary.uploader.upload(
        "ex.png", folder="retinopathy/" + str(identifier)
    )

    # print(upload_result)
    response = {"resultimage": upload_result["secure_url"]}
    # print(response['resultimage'])
    return jsonify(response)


@app.route("/Micro", methods=["POST"])
def Micro():
    # tf.compat.v1.disable_eager_execution()
    message = request.get_json(force=True)
    image_url = message["originalimage"]
    identifier = message["identifier"]
    # input_img = imread(image_url)
    out_img = predict_ma(image_url)
    out_img.save("micro.png")

    upload_result = cloudinary.uploader.upload(
        "micro.png", folder="retinopathy/" + str(identifier)
    )

    # print(upload_result)
    response = {"resultimage": upload_result["secure_url"]}
    # print(response['resultimage'])
    return jsonify(response)


@app.route("/softExudates", methods=["POST"])
def softExudates():
    # tf.compat.v1.disable_eager_execution()
    message = request.get_json(force=True)
    image_url = message["originalimage"]
    identifier = message["identifier"]
    # input_img = imread(image_url)
    out_img = predict_se(image_url)
    out_img.save("se.png")

    upload_result = cloudinary.uploader.upload(
        "se.png", folder="retinopathy/" + str(identifier)
    )

    # print(upload_result)
    response = {"resultimage": upload_result["secure_url"]}
    # print(response['resultimage'])
    return jsonify(response)


@app.route("/hemorrage", methods=["POST"])
def hemorrage():
    # tf.compat.v1.disable_eager_execution()
    message = request.get_json(force=True)
    image_url = message["originalimage"]
    identifier = message["identifier"]
    # input_img = imread(image_url)
    out_img = predict_he(image_url)
    out_img.save("hemo.png")

    upload_result = cloudinary.uploader.upload(
        "hemo.png", folder="retinopathy/" + str(identifier)
    )

    # print(upload_result)
    response = {"resultimage": upload_result["secure_url"]}
    # print(response['resultimage'])
    return jsonify(response)


if __name__ == "__main__":
    app.run()
