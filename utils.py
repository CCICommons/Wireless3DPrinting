from subprocess import Popen, PIPE
from flask import Markup


ALLOWED_EXTENSIONS = {"3w"}


def get_output(command):
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    process.wait();
    return stdout.decode("utf-8")

def to_template_safe(input):
    return Markup(input.replace('\n', '<br>'))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS