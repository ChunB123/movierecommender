import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import pickle
import random
import logging
from logging.handlers import RotatingFileHandler
import requests
from flask import Flask
import ldclient
from ldclient import Context
from ldclient.config import Config
from canary_release_utils import is_sdk_initialized, get_average_response_time
from src.email_util import send_email

app = Flask(__name__)

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(handler)


current_version = "0"
user_movies = {}
info = {}
common_movies = {}


try:
    ldclient.set_config(Config("sdk-d1e9c289-278d-40ad-9773-79ad3eb42e83"))
    is_sdk_initialized(app)
except Exception as e:
    app.logger.warning("LaunchDarkly Error: ", e)

def curl_req(link: str):
    response = None
    try:
        response = requests.get(link)
    except:
        return False, None

    if 'message' in response:
        return False, None

    return True, response.json()


@app.route('/recommend/<string:user_id>')
def recommendation_route(user_id):
    if int(user_id) < 0 or int(user_id) > 1000*1000: return "Invalid user"
    movies = []

    recommendation_version = ""

    try:
        context = Context.builder(user_id).build()
        # Versions: 1, 2, 3...
        recommendation_version = ldclient.get().variation("model_version", context, current_version)
    except Exception as e:
        app.logger.warning("LaunchDarkly Error: ", e)

    app.logger.warning("recommendation_version: " + recommendation_version)

    if user_id in user_movies[recommendation_version]:
        movies = user_movies[recommendation_version][user_id]
    else:
        random.seed(user_id)
        movies = common_movies[recommendation_version][random.randint(0, 99)]

    response = ",".join(movies)
    new_log = {"userid": user_id, "model_version": info["model_version"], "training_data_version": info["training_data_version"], "pipeline_version": info["pipeline_version"], "response": response}
    logger.info(new_log)

    return response

@app.route('/release_test_run/<string:old_version_id>/<string:new_version_id>')
def release_test_run_route(old_version_id, new_version_id):
    # Check response time (10 mins)
    average_response_time = get_average_response_time("http://localhost:8082/recommend/1")
    # Check Click-Through Rate (CTR, 30 mins)
    # After two checks, write the log (old_version_id and new_version_id)
    # and send email
    if average_response_time > 0.5:
        # Send aborting email
        send_email("Please abort this release, version: " + current_version)
    else:
        send_email("Please continue this release, version: " + current_version)
    return str(average_response_time)


if __name__ == '__main__':
    info_file = "../data/info/info.pkl"

    with open(info_file, 'rb') as file:
        info = pickle.load(file)

    current_version = info["recommendation_version"]
    previous_version = current_version - 1
    current_version = str(current_version)
    previous_version = str(previous_version)

    user_movies_file_previous = "../data/recommendation_versions/recommendation_user_" + previous_version + ".pkl"
    user_movies_file_current = "../data/recommendation_versions/recommendation_user_" + current_version + ".pkl"
    with open(user_movies_file_previous, 'rb') as file:
        user_movies[previous_version] = pickle.load(file)
    
    with open(user_movies_file_current, 'rb') as file:
        user_movies[current_version] = pickle.load(file)


    common_movies_file_previous = "../data/recommendation_versions/common_movies_" + previous_version + ".pkl"
    common_movies_file_current = "../data/recommendation_versions/common_movies_" + current_version + ".pkl"
    with open(common_movies_file_previous, 'rb') as file:
        common_movies[previous_version] = pickle.load(file)
    
    with open(common_movies_file_current, 'rb') as file:
        common_movies[current_version] = pickle.load(file)

    app.run(host='0.0.0.0', port=8082)