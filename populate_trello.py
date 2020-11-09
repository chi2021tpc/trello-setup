import csv
import os
import requests
import sys
import yaml

# ------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print("Usage: python preprocess_csv.py [/path/to/input/preprocessed-data.csv] [/path/to/output/yaml]")
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

board_desc = "This Trello board is for managing the status of each submission and also creating paper groups for session organization."

list_names = [
    "Not Discussed Yet",
    "Accepted (Not Grouped Yet)",
    "Rejected",
    "Tabled",
    "Accepted (Session: XXX)",
    "Accepted (Session: YYY)",
    "Accepted (Session: ZZZ)",
]

# ------------------------------------------------------------------------------

def extract_subcommittee_track_list(data):
    subcommittee_set = set()
    for row in data:
        subcommittee_set.add(row["Subcommittee"])
    return sorted(subcommittee_set)

with open(input_path, newline='', encoding = "utf-8-sig") as csv_file:
    reader = csv.DictReader(csv_file)
    submission_data = [row for row in reader]

subcommittee_track_list = extract_subcommittee_track_list(submission_data)

print("#tracks: {}".format(len(subcommittee_track_list)))

# ------------------------------------------------------------------------------

trello_data = {}

for track in subcommittee_track_list:
    board_name = track + " - CHI 2021"

    if not "Modalities A" in track:
        continue

    # --------------------------------------------------------------------------

    # https://developer.atlassian.com/cloud/trello/rest/#api-members-id-boards-get
    result = requests.get(base_url + "members/me/boards?key={}&token={}".format(key, token))

    if result.status_code != 200:
        print(result, result.reason)
        exit(0)

    for board_info in result.json():
        if board_info["name"] == board_name:
            print("Warning: The specified board name is already used in existing (either open or closed) boards.")

    # --------------------------------------------------------------------------

    # https://developer.atlassian.com/cloud/trello/rest/#api-boards-post
    data = {
        "name": board_name,
        "defaultLabels": "true",
        "defaultLists": "false",
        "desc": board_desc,
        "prefs_permissionLevel": "private",
        "prefs_voting": "disabled",
        "prefs_comments": "disabled",
        "prefs_invitations": "admins",
        "prefs_selfJoin": "true",
        "prefs_cardCovers": "false",
        "prefs_background": "grey",
        "prefs_cardAging": "regular",
        "key": key,
        "token": token,
    }

    result = requests.post(base_url + "boards", data=data)

    if result.status_code != 200:
        print(result, result.reason)
        exit(0)

    board_id = result.json()["id"]
    board_url = result.json()["shortUrl"]

    print("Message: Created a new board (board_id = {})".format(board_id))

    # --------------------------------------------------------------------------

    first_list_id = ""
    for list_name in list_names:
        # https://developer.atlassian.com/cloud/trello/rest/#api-boards-id-lists-post
        data = {
            "name": list_name,
            "pos": "bottom",
            "key": key,
            "token": token,
        }

        result = requests.post(base_url + "boards/{}/lists".format(board_id), data=data)

        if result.status_code != 200:
            print(result, result.reason)
            exit(0)

        list_id = result.json()["id"]

        if not first_list_id:
            assert list_name is "Not Discussed Yet"

            first_list_id = list_id

        print("Message: Created a new list (list_id = {})".format(list_id))

    # --------------------------------------------------------------------------

    for row in submission_data:
        if row["Subcommittee"] != track:
            continue

        card_name = "[{}] {}".format(row["Paper ID"], row["Title"])
        card_desc = "### Abstract:\n{}\n\n### Keywords:\n- {}\n\n### First Author's Country/Region (for Session Scheduling):\n{}".format(row["Abstract"], row["Key Words"].replace(";", "\n- "), row["Author 1 - country 1"])

        # https://developer.atlassian.com/cloud/trello/rest/#api-cards-post
        data = {
            "name": card_name,
            "desc": card_desc,
            "idList": first_list_id,
            "key": key,
            "token": token,
        }
        result = requests.post(base_url + "cards", data=data)

        if result.status_code != 200:
            print(result, result.reason)
            exit(0)

        card_id = result.json()["id"]
        print("Message: Created a new card (card_id = {})".format(card_id))

    # --------------------------------------------------------------------------

    trello_data[track] = {
        "track_name": track,
        "board_id": board_id,
        "board_url": board_url,
    }

# ------------------------------------------------------------------------------

with open(output_path, 'w') as yaml_file:
    yaml.dump(trello_data, yaml_file)

# ------------------------------------------------------------------------------

print("Message: Done.")
