from http import HTTPStatus

import trafaret as t
from flask_cors import CORS
from flask import Flask, jsonify

from handlers.api import mine_field
from handlers.response_messages import MessageType

app = Flask(__name__)
app.register_blueprint(mine_field.bp, url_prefix="/mine_field")
CORS(app)


@app.route("/", methods=["GET"])
def index_route():
    return jsonify({"message": MessageType.ServiceHealth.value})


@app.errorhandler(t.DataError)
def handle_validation_violations(error):
    return jsonify(
        {"message": MessageType.ValidationError.value, "error": error.as_dict()}
    ), HTTPStatus.UNPROCESSABLE_ENTITY


@app.errorhandler(400)
def handle_bad_requests(error):
    return jsonify(
        {"message": MessageType.RequestError.value, "error": "unable to parse json payload"}
    ), HTTPStatus.BAD_REQUEST


@app.errorhandler(404)
def handle_not_found_page_requests(error):
    return jsonify({"message": MessageType.NotFound.value, "error": f"{error}".lower()}), HTTPStatus.NOT_FOUND


@app.errorhandler(405)
def handle_not_found_method_requests(error):
    return jsonify(
        {"message": MessageType.NotAllowed.value, "error": f"{error}".lower()}
    ), HTTPStatus.METHOD_NOT_ALLOWED


@app.errorhandler(500)
def handle_server_errors(error):
    return jsonify(
        {"message": MessageType.ServerError.value, "error": "failed to process the request"}
    ), HTTPStatus.INTERNAL_SERVER_ERROR
