import os
import requests
import sys
import yaml
import json

# ------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print("Usage: python get_status.py /path/to/input/yaml /path/to/output/csv")
    exit(0)

input_path = sys.argv[1]
output_path = sys.argv[2]

# ------------------------------------------------------------------------------

config_path = os.path.dirname(os.path.abspath(__file__)) + "/config/config.yml"

with open(config_path, 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

key = config["key"]
token = config["token"]

# ------------------------------------------------------------------------------

base_url = "https://api.trello.com/1/"

# ------------------------------------------------------------------------------

with open(input_path, 'r') as file:
    board_data = json.load(file)

board_ids = [entry["board_id"] for entry in board_data]

# ------------------------------------------------------------------------------

def get_boards():
    # https://developer.atlassian.com/cloud/trello/rest/#api-members-id-boards-get
    result = requests.get(base_url + "members/me/boards?key={}&token={}&fields=name,url".format(key, token))

    if result.status_code != 200:
        print(result, result.reason)
        assert False

    # Display existing boards in JSON format
    if False:
        print("[")
        for entry in result.json():
            print("  {{ \"board_id\": \"{}\", \"name\": \"{}\" }},".format(entry["id"], entry["name"]))
        print("]")

    return result.json()


def get_lists(board_id):
    # https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get
    result = requests.get(base_url + "boards/{}/lists?key={}&token={}&fields=name".format(board_id, key, token))

    if result.status_code != 200:
        print(result, result.reason)
        assert False

    return result.json()


def get_cards_in_list(list_id):
    # https://developer.atlassian.com/cloud/trello/rest/api-group-lists/#api-lists-id-cards-get
    result = requests.get(base_url + "lists/{}/cards?key={}&token={}&fields=name".format(list_id, key, token))

    if result.status_code != 200:
        print(result, result.reason)
        assert False

    return result.json()


boards = get_boards()

data = []

for board_info in boards:

    if board_info["id"] in board_ids:
        print(board_info["name"])

        track_data = {}
        track_data["name"] = board_info["name"]
        track_data["lists"] = []
        track_data["url"] = board_info["url"]

        lists = get_lists(board_info["id"])
        for list in lists:
            cards = get_cards_in_list(list["id"])
            track_data["lists"].append({ "name": list["name"], "num": len(cards) })

        data.append(track_data)

csv = ""

for track_data in data:
    csv += "\"{}\",{}\n".format(track_data["name"], track_data["url"])
    for list_data in track_data["lists"]:
        csv += "\"{}\",{}\n".format(list_data["name"], list_data["num"])
    csv += ",\n"

with open(output_path, 'w') as file:
    file.write(csv)

print("Message: Done.")
