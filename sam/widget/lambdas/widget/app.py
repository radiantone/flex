import awsgi
from example.models import Widget
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/widget/<id>")
def widget(id):

    widget = Widget.find({'id': id})

    return jsonify(widget[0])


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})
