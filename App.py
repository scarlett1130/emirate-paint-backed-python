from crypt import methods
import cv2

import img_proc
from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS, cross_origin
from PIL import Image
import numpy as np
from io import BytesIO

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


@app.route("/", methods=["GET"])
def status_check():
    return jsonify(status = "OK")

@app.route("/predict", methods=['POST'])
@cross_origin()
def change_color():
    file1 = request.files['org_image']
    org_img = Image.open(file1.stream)

    file2 = request.files['new_image']
    new_img = Image.open(file2.stream)

    r = int(request.form['r'])
    g = int(request.form['g'])
    b = int(request.form['b'])
    x = int(request.form['x'])
    y = int(request.form['y'])
    width = int(request.form['width'])
    height = int(request.form['height'])
    color = [r, g, b]
    position = (x, y)

    org_img = np.array(org_img)
    org_img = cv2.resize(org_img, (width, height))
    new_img = np.array(new_img)
    new_img = cv2.resize(new_img, (width, height))

    final_img = img_proc.changeColor(org_img=org_img, new_img=new_img, position=position, color=color)
    final_img = Image.fromarray(final_img)

    return serve_pil_image(final_img)


if __name__ == '__main__' :
    print('Application Started .......')
    app.run()
