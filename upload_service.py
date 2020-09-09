from eventlet import wsgi
import eventlet
eventlet.monkey_patch()
from flask import Flask, request, send_file, render_template
from uuid import uuid4
import io
from time import time

app = Flask(__name__)

@app.route('/up', methods=['GET'])
def upload_service():
    return render_template("upload.html")

wsgi.server(eventlet.listen(('', 56002)), app)
