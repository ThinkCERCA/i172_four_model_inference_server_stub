from traceback import format_exc
from flask import Flask, request
from flask_cors import CORS, cross_origin
from swa_lib.configs import configuration
from swa_lib.log import log
from swa_lib.models import models
from swa_lib.errors import Errors

configuration.__init__()
models.__init__(configuration)
app = Flask(__name__)
CORS(app)


@app.route("/api/predict", methods=['GET', 'POST'])
@cross_origin()
def predict():
    if request.method != 'POST':
        return Errors.ONLY_POST_REQUESTS_ALLOWED
    opt_dict = dict()
    result_dict = dict()
    error_msg = ''
    try:
        opt_dict = request.get_json()
        result_dict = models.predict(request.get_json())
    except Exception:
        result_dict = Errors.UNDEFINED_ERROR
        error_msg = format_exc()
    finally:
        log_str = f"Options:\n{opt_dict}\nResult:\n{result_dict}"
        if error_msg:
            log_str += f"\nError:\n{error_msg}"
        log.debug(log_str)
        return result_dict


@app.route("/api/list_models", methods=['GET', 'POST'])
@cross_origin()
def list_models():
    """
    List models.
    Example result:{
      'default': 'model_1',
      'models': [
        {'full_name': 'Some Model 1', 'name': 'model_1', 'type': 'score_result'},
        {...}
      ]
    }
    """
    return {
        'models': [{'name': x.name, 'full_name': x.full_name, 'type': x.type} for x in configuration.models],
        'default': models.default_model_name
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=configuration.get_value('server', 'port', 8008, int), debug=False)
