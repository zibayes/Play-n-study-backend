from flask import Blueprint

api = Blueprint('api', __name__)


@api.route('/api')
def api():
    return "this is example"
