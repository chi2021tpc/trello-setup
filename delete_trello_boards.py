import os
import requests
import sys
import yaml

# ------------------------------------------------------------------------------

if len(sys.argv) < 1:
    print("Usage: python preprocess_csv.py /path/to/input/yaml")
    exit(0)

input_path = sys.argv[1]

# ------------------------------------------------------------------------------

config_path = os.path.dirname(os.path.abspath(__file__)) + "/config/config.yml"

with open(config_path, 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

key = config["key"]
token = config["token"]

# ------------------------------------------------------------------------------

base_url = "https://api.trello.com/1/"

# ------------------------------------------------------------------------------

with open(input_path, 'r') as yml:
    board_data = yaml.load(yml, Loader=yaml.FullLoader)

board_ids = [entry["board_id"] for entry in board_data.values()]

# ------------------------------------------------------------------------------

# https://developer.atlassian.com/cloud/trello/rest/#api-members-id-boards-get
result = requests.get(base_url + "members/me/boards?key={}&token={}".format(key, token))

if result.status_code != 200:
    print(result, result.reason)
    exit(0)

# print(board_ids)
# print([entry["id"] for entry in result.json()])

for board_info in result.json():

    if board_info["id"] in board_ids:

        board_id = board_info["id"]

        # https://developer.atlassian.com/cloud/trello/rest/#api-boards-id-delete
        result = requests.delete(base_url + "boards/{}?key={}&token={}".format(board_id, key, token))

        if result.status_code != 200:
            print(result, result.reason)
            exit(0)

        print("Message: Deleted a board (board_id = {}).".format(board_id))

print("Message: Done.")
