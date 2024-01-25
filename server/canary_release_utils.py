import ldclient
import requests
import time
import json
import logging

logging.basicConfig(level=logging.INFO)


def is_sdk_initialized(app):
    if ldclient.get().is_initialized():
        app.logger.info("SDK successfully initialized!")
    else:
        app.logger.info("SDK failed to initialize")


project_key = "default"
feature_flag_key = "model_switch"
api_key = ""
url = "https://app.launchdarkly.com/api/v2/flags/" + project_key + "/" + feature_flag_key


def get_variationids_list():
    headers = {"Authorization": api_key}

    response = requests.get(url, headers=headers)

    data = response.json()
    variation_ids = [variation["_id"] for variation in data["variations"]]
    print(variation_ids)
    return variation_ids


def percentage_roll_out(old_version, new_version, new_version_percentage):
    payload = {
        "environmentKey": "production",
        "instructions": [{"kind": "turnFlagOff"}]
    }

    headers = {
        "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
        "Authorization": api_key
    }

    response = requests.patch(url, json=payload, headers=headers)

    data = response.json()
    print(data)
    return 0


def get_average_response_time(api_url, duration_minutes=0.5, interval_seconds=1):
    total_time = 0
    num_requests = 0
    end_time = time.time() + duration_minutes * 60

    while time.time() < end_time:
        start_time = time.time()
        try:
            response = requests.get(api_url, timeout=2)
        except:
            return 2
        response_time = time.time() - start_time
        logging.info(str(response_time) + " " + str(response))

        total_time += response_time
        num_requests += 1
        time.sleep(interval_seconds)

    return total_time / num_requests if num_requests > 0 else 0


if __name__ == '__main__':
    # Test CD num_1
    # get_variationids_list()
    # percentage_roll_out(1, 2, 0.2)
    url = ""
    average_response_time = get_average_response_time(url)
    print(f"Average response time: {average_response_time} seconds")
