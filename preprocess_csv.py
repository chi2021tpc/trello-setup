import csv
import sys

if len(sys.argv) < 3:
    print("Usage: python preprocess_csv.py [/path/to/input/csv] [/path/to/output/csv]")
    exit(0)

input_path = sys.argv[1]
output_path = sys.argv[2]

csv.field_size_limit(sys.maxsize)

# Load data from the csv file
# Note: specifyinig "utf-8-sig" is necessary to properly handle the BOM "\ufeff" at the beginning of the csv document
with open(input_path, newline='', encoding = "utf-8-sig") as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

