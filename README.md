# trello-setup

Scripts for Trello

- `preprocess_csv.py`: (TODO)
- `populate_trello.py`: (TODO)

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

## Environment

- Python 3.6+
