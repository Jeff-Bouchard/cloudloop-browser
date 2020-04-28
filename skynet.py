#THIS RUNS ON GCP - https://us-central1-cloudloop-175221.cloudfunctions.net/upload-to-skynet
# (c) Zip Technologies LLC 2020

from siaskynet import Skynet
from uuid import uuid4
from flask import request
from flask.json import jsonify

from app import app


@app.route('/skynet', methods=['POST'])
def upload_to_skynet():
    data_to_upload = request.get_data()
    filename = f'cloudloop-file-{uuid4()}.wav'
    with open(filename, 'wb') as f:
        f.write(data_to_upload)
    skylink = Skynet.upload_file(filename)
    print("Upload successful, skylink: " + skylink)
    return jsonify(skylink)