from flask import Flask
from flask import jsonify, send_from_directory
import os
import re

app = Flask(__name__)
base_dir = os.getcwd() + "/"


@app.route('/')
def hello_world():
    print os.getcwd()
    return 'Hello World!'


@app.route('/download/<file_name>')
def download(file_name):
    file_path = base_dir + "latestJSBundle/" + file_name
    if os.path.exists(file_path):
        return send_from_directory(base_dir, "latestJSBundle/" + file_name, as_attachment=True)
    else:
        return "file not exists"


@app.route('/update/<version_name>')
def update(version_name):
    latest_version_name = '1.0.0.0'

    bundle_files = os.listdir(base_dir + "latestJSBundle")
    if len(bundle_files) > 0:
        latest_version_name = bundle_files[0]

    print "latest_version: " + latest_version_name
    update = need_update(version_name, latest_version_name)
    if update:
        download_url = "http://192.168.73.90:5000/download/" + latest_version_name
    else:
        download_url = ""

    response = {
        'needUpdate': update,
        'latestVersion': latest_version_name,
        'signature': '',
        'downloadUrl':download_url
    }

    return jsonify(response)


def need_update(current_version_name, latest_version_name):
    regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
    match = regex.match(current_version_name)
    if not match:
        return False
    match = regex.match(latest_version_name)
    if not match:
        return False

    current_code = get_version_code(current_version_name)
    latest_code = get_version_code(latest_version_name)

    if latest_code > current_code:
        return True
    else:
        return False


def get_version_code(version_name):
    arr = version_name.split(".")
    arr.reverse()
    code = 0
    weight = 1
    for str in arr:
        code  = code + weight * int(str)
        weight = weight * 10
    return code


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
