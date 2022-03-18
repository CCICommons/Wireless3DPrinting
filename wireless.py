from flask import Flask, flash, request, redirect, send_from_directory, url_for
from flask import render_template

import os

import utils

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

device_dict = {}

@app.route("/")
def home():
    output = utils.to_template_safe(utils.get_output(['miniMover/miniMoverConsole/minimover']))
    return render_template('home.html', description=output)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and utils.allowed_file(file.filename):
            filename = file.filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            device = device_dict[request.form['printers']]

            utils.get_output(f'miniMover/miniMoverConsole/minimover -d {device} -p "{path}"')
            
            # return redirect(url_for('download_file', name=filename))
            return redirect(url_for('status', device_id=device))
    
    output = utils.get_output('ls /dev/ttyACM*')
    device_list = output.split('\n')

    for device in device_list:
        if device.startswith('/dev'):
            output = utils.get_output(f'miniMover/miniMoverConsole/minimover -d {device} -s')

            for item in output.split("\n"):
                if 'printer name:' in item:
                    device_dict[item.split(': ')[1].strip()] = device
                    break

    return render_template('upload.html', devices=device_dict.items())

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route("/devices")
def all_devices():
    output = utils.get_output('ls /dev/ttyACM*')
    device_list = output.split('\n')

    for device in device_list:
        if device.startswith('/dev'):
            output = utils.get_output(f'miniMover/miniMoverConsole/minimover -d {device} -s')

            for item in output.split("\n"):
                if 'printer name:' in item:
                    device_dict[item.split(': ')[1].strip()] = device
                    break

    return render_template('home.html', description=output)

@app.route("/status/<path:device_id>")
def status(device_id):
    output = utils.to_template_safe(utils.get_output(f'miniMover/miniMoverConsole/minimover -d /{device_id} -s'))
    return render_template('home.html', description=output)

if __name__ == "__main__":
    app.run()