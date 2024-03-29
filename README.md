# trello-setup

Scripts for Trello.

- `preprocess_csv.py`: (TODO)
- `populate_trello.py`: (TODO)
- `monitor_boards.py`: (TODO)
- `dump_accepted_papers.py`: This script is used after the PC meetings to retrieve the list of all accepted papers from Trello Boards edited by ACs/SCs. By running this script, we can get `all.csv` that contains all information about the accepted papers.
- `dump_organized_papers.py`: This script is used to retrieve the list of all accepted papers, each of which is associated with a certain session name, day, and room, from Trello Boards edited by the TPC team. By running this script, we can get another `all.csv` (sorry for using the confusing file name).

## How to Use

### Preparation

Get the Trello key and token.

Edit `config/config.yml`.

### Before PC Meetings

Download `Submission.csv` and `chi21b_submission.csv` from PCS.

```bash
python preprocess_csv.py /path/to/input/chi21b_submission.csv /path/to/input/Submission.csv /path/to/output/preprocessed-data.csv
```

```bash
python populate_trello.py /path/to/input/preprocessed-data.csv /path/to/output/trello.yml
```

### During PC Meetings

During the PC meeting period, TPCs need to monitor the progress of session forming:
```bash
python monitor_boards.py /path/to/input/json /path/to/output/csv
```
where the json file should be a list of boards that will be monitored:
```json
[
  { "board_id": "(board_id)", "name": "Accessibility and Aging - CHI 2021" },
  { "board_id": "(board_id)", "name": "Computational Interaction - CHI 2021" },
  { "board_id": "(board_id)", "name": "Critical and Sustainable Computing - CHI 2021" },
  { "board_id": "(board_id)", "name": "Design A - CHI 2021" },
  ...
]
```

### After PC Meetings

After the PC meeting, we can retrieve the list of accepted papers and export it as a CSV file:
```bash
python dump_accepted_papers.py /path/to/input/json /path/to/output/dir
```
then we can obtain `all.csv`.

After the TPC team edited Trello Boards appropriately (editing session names, merging some sessions, moving some papers to different sessions, adding session days and rooms), we can retrieve the list of accepted papers with additional information (day and room) and export it as another CSV file:
```bash
python dump_organized_papers.py /path/to/input/json /path/to/original/all.csv /path/to/output/dir
```
where `/path/to/original/all.csv` is the CSV file that we already generated by using `dump_accepted_papers.py`. Then, we can obtain another `all.csv`.

Note that Trello Boards edited by the TPC team should look like this:

<img width="1440" alt="Screen Shot 2022-01-07 at 10 48 51" src="https://user-images.githubusercontent.com/2696321/148478272-dd8bad90-b0be-4ca0-af42-ed6bbd20717d.png">

where each list name has a prefix like `2-1` (`2` indicates the room and `1` indicates the day in this case).

## Environment

- Python 3.6+
