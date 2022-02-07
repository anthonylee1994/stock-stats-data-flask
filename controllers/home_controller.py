from flask import Blueprint, jsonify


home_controller = Blueprint('home_controller', __name__)


@home_controller.route('/')
def index():
    return jsonify({'stock-stats-data-python': 'V1.0'})
