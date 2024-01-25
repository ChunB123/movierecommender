import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
import datetime
import random

from monitering_utils import get_project_root

def rewrite_log_file(filename):
    try:
        # rewrites = 0
        while True:
            with open(filename, 'r+') as file:

                lines = file.readlines()
                if lines:
                    # first_line = str(rewrites)+lines[0]
                    first_line = lines[0]
                    file.write(first_line)
                    file.flush()
                    print("Write down something!")
                else:
                    print("File is empty!")

            time.sleep(180)
            # rewrites += 1
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    filename = os.path.join(get_project_root(), "data/eval_user_result.txt")
    print(filename)
    rewrite_log_file(filename)