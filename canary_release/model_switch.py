from datetime import datetime

import ldclient
from ldclient import Context
from ldclient.config import Config
import random
import time


# Create a helper function for rendering messages.
def show_message(s):
    print("*** %s" % s)
    print()


# Initialize the ldclient with your environment-specific SDK key.
if __name__ == "__main__":
    sdk_key = ""
    ldclient.set_config(Config(sdk_key))

    if ldclient.get().is_initialized():
        show_message("SDK successfully initialized!")
    else:
        show_message("SDK failed to initialize")
        exit()

    while True:
        # Simulating different random users
        user_key = 'user-' + str(datetime.now())
        context = Context.builder(user_key).build()

        new_model = ldclient.get().variation("model_version", context, 1)
        show_message(str(new_model) + " is enabled for user %s" % user_key)
        time.sleep(0.5)

"""
    # Evaluate the feature flags for Model A and Model B
    new_model = ldclient.get().variation("model_switch", context, False)
    if new_model:
        show_message("new_model is enabled for user %s" % user_key)
    else:
        show_message("old_model is enabled for user %s" % user_key)
"""
# Ensure that the SDK shuts down cleanly
ldclient.get().close()
