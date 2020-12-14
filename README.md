# trello-setup

Scripts for Trello

- `preprocess_csv.py`: (TODO)
- `populate_trello.py`: (TODO)
- `monitor_boards.py`: (TODO)

## Run

Get the Trello key and token.

Edit `config/config.yml`.

Download `Submission.csv` and `chi21b_submission.csv` from PCS.

```bash
python preprocess_csv.py /path/to/input/chi21b_submission.csv /path/to/input/Submission.csv /path/to/output/preprocessed-data.csv
```

```bash
python populate_trello.py /path/to/input/preprocessed-data.csv /path/to/output/trello.yml
```

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

## Environment

- Python 3.6+
