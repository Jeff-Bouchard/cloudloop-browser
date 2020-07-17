from siaskynet import Skynet
from flask.json import jsonify
from flask import request, Flask
from uuid import uuid4
import wavy
from airtable import Airtable
import os

app = Flask(__name__)

def get_wav_data(filename):
    print(f'Opening wav file: {filename}')
    data = {}
    f = wavy.info(filename)
    data['channels'] = f.n_channels
    data['samplewidth'] = f.sample_width
    data['samplerate'] = f.framerate
    data['samples'] = f.n_frames
    print(f'Got wav data from {filename}')
    return data



def get_upload_options():
        return type('obj', (object,), {
            'portal_url': 'https://skynet.cloudloop.io',
            'portal_upload_path': 'skynet/skyfile',
            'portal_file_fieldname': 'file',
            'portal_directory_file_fieldname': 'files[]',
            'custom_filename': ''
        })

@app.route('/upload', methods=['POST'])
def upload_to_skynet():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # upload
    data_to_upload = request.get_data()
    print(f'Got {len(data_to_upload)} bytes to upload')
    filename = f'/tmp/cloudloop-file-{uuid4()}.wav'
    with open(filename, 'wb') as f:
        f.write(data_to_upload)
    file_data = get_wav_data(filename)
    print(f'Analyzed file {filename} : {file_data}')
    skylink = Skynet.upload_file(filename, get_upload_options())
    airtable_records =  {'link': skylink,
                         'samples': file_data['samples'],
                         'sample_rate': file_data['samplerate'],
                         'bit_depth': file_data['samplewidth'],
                         'channels': file_data['channels']}
    print(f'Analyzed file {filename} : {airtable_records}')
    airtable = Airtable('appHcObTX28Vj70uM', 'Loops', api_key='keypPtZeMX7BJDv9f')
    airtable.insert(airtable_records)
    print("Upload successful, skylink: " + skylink)
    return jsonify(skylink)
