from flask import Flask, jsonify
from lib.exception.api_exception import ApiException
from routes.drop_token import drop_token_bp


app = Flask(__name__)
app.register_blueprint(drop_token_bp)


@app.errorhandler(ApiException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
