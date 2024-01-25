import os
import sys
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
import datetime
import random

from monitering_utils import get_project_root


def test_get_project_root():
    root = get_project_root()
    print(root)


def generate_fake_log():
    log_level = random.choice(["INFO", "ERROR", "WARNING", "DEBUG"])
    user_id = random.randint(1000, 9999)
    operation = random.choice(["LOGIN", "LOGOUT", "OPERATION_A", "OPERATION_B"])
    return f"{datetime.datetime.now()} - {log_level} - User:{user_id} performed {operation}"


def main():
    log_file_path = os.path.join(get_project_root(), "data/fake_logs.txt")
    while True:
        with open(log_file_path, "w") as file:
            file.write(generate_fake_log() + "\n")
            file.flush()
            print("Generated some test log")
        time.sleep(5)


def rewrite_log_file(filename):
    try:
        rewrites = 0
        while True:
            with open(filename, 'r+') as file:

                lines = file.readlines()
                if lines:
                    first_line = str(rewrites)+lines[0]
                    # first_line = lines[0]
                    file.write(first_line)
                    file.flush()
                else:
                    print("File is empty!")

            time.sleep(2)
            rewrites += 1
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # test_get_project_root()
    filename = os.path.join(get_project_root(), "data/eval_user_result.txt")
    rewrite_log_file(filename)
