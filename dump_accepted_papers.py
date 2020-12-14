import os
import requests
import sys
import yaml
import json
import re
import csv

# ------------------------------------------------------------------------------

if len(sys.argv) < 2:
    print("Usage: python dump_accepted_papers.py /path/to/input/json /path/to/output/dir")
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
pcs_submission_url_template = "https://new.precisionconference.com/chi21b/chair/subs/{}"

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
    result = requests.get(base_url + "lists/{}/cards?key={}&token={}&fields=name,desc".format(list_id, key, token))

    if result.status_code != 200:
        print(result, result.reason)
        assert False

    return result.json()


boards = get_boards()

# data = []

ignore_keywords = [
    "Rejected",
    "Not Discussed Yet",
    "Withdrawn",
    "Withdraw",
    "withdrawn",
    "Not Yet Discussed",
    "Stored, Ignore",
]

keys = [
    "subcommittee/track",
    "session title (TPC)",
    "session title (original)",
    "submission id",
    "title",
    "author region",
    "URL",
    "Note",
]

all_output_csv_path = "{}/all.csv".format(output_path)
all_writer = csv.writer(open(all_output_csv_path, 'w'))
all_writer.writerow(keys)

for board_info in boards:

    if board_info["id"] in board_ids:
        print(board_info["name"])

        track_data = {}
        track_data["name"] = board_info["name"]
        track_data["lists"] = []
        track_data["url"] = board_info["url"]

        lists = get_lists(board_info["id"])
        for list in lists:
            should_be_ignored = False
            for ignore_keyword in ignore_keywords:
                if ignore_keyword in list["name"]:
                    print("- List (\"{}\") is skipped.".format(list["name"]))
                    should_be_ignored = True

            if should_be_ignored:
                continue

            cards = get_cards_in_list(list["id"])
            track_data["lists"].append({ "name": list["name"], "cards": cards })

        # data.append(track_data)

        track_name = track_data["name"].replace(" - CHI 2021", "")

        output_csv_path = "{}/{}.csv".format(output_path, track_name)
        file = open(output_csv_path, 'w')
        writer = csv.writer(file)
        writer.writerow(keys)

        for list in track_data["lists"]:
            for card in list["cards"]:
                session_name = list["name"]

                match = re.fullmatch(r"Accepted\s\(Session:\s(.+)\)", session_name)
                if match:
                    session_name = match.groups()[0]
                match = re.fullmatch(r"Accepted:\s(.+)", session_name)
                if match:
                    session_name = match.groups()[0]
                match = re.fullmatch(r"[0-9][0-9]\s-\s(.+)", session_name)
                if match:
                    session_name = match.groups()[0]

                submission_id = re.search("\[pn([0-9]+)\]", card["name"]).groups()[0]
                title = re.split("\[pn[0-9]+\] ", card["name"])[1].replace("\"", "\\\"")
                region = card["desc"].split("(for Session Scheduling):\n")[1]
                detail = pcs_submission_url_template.format(submission_id)

                writer.writerow([track_name, session_name, session_name, submission_id, title, region, detail, ""])
                all_writer.writerow([track_name, session_name, session_name, submission_id, title, region, detail, ""])

print("Message: Done.")
