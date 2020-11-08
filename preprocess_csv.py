import csv
import sys

if len(sys.argv) < 3:
    print("Usage: python preprocess_csv.py [/path/to/input/chi21b_submission.csv] [/path/to/input/Submissions.csv] [/path/to/output/csv]")
    exit(0)

input_1_path = sys.argv[1]
input_2_path = sys.argv[2]
output_path = sys.argv[3]

csv.field_size_limit(sys.maxsize)

def load_data_1(path):
    # Load data from the csv file
    # Note: specifyinig "utf-8-sig" is necessary to properly handle the BOM "\ufeff" at the beginning of the csv document
    with open(path, newline='', encoding = "utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]

        # Delete irrelevant submissions
        print("The number of submissions: {}".format(len(data)))
        data = [row for row in data if not "incomplete" in row["Status"]]
        data = [row for row in data if not "QR" in row["Decision"]]
        data = [row for row in data if not "DR" in row["Decision"]]
        print("The number of submissions to be discussed in the PC meeting: {}".format(len(data)))

        # Delete irrelevant data columns
        keys_to_be_deleted = [
            "Contact Name",
            "Contact Email",
            "Note",
            "Decision",
            "Overall Score", "Comments to Authors", "Rebuttal", "The Document in PDF", "The Document in PDF pages", "The Document in PDF paper size", "(Optional) Video Figure", "(Optional) Supplementary Material (in a ZIP file)", "Related Concurrent Submissions", "Did you add your dblp-link or equivalent to your PCS profile", "Accessibility of figures/Alternative text for all figures and tables", "Anonymity Check", "Description of Supplementary Files", "(Optional) External Reviewer Recommendations", "Agreement to review", "CHI 2021 Submitter Agreement", "Proposed new future CHI sub committee",
            "Author 1 - id", "Author 1 - prefix", "Author 1 - first", "Author 1 - middle", "Author 1 - last", "Author 1 - suffix", "Author 1 - email", "Author 1 - dept/school/lab 1", "Author 1 - institution 1", "Author 1 - city 1", "Author 1 - state/prov 1", "Author 1 - country 1", "Author 1 - dept/school/lab 2", "Author 1 - institution 2", "Author 1 - city 2", "Author 1 - state/prov 2", "Author 1 - country 2",
            "Author 2 - id", "Author 2 - prefix", "Author 2 - first", "Author 2 - middle", "Author 2 - last", "Author 2 - suffix", "Author 2 - email", "Author 2 - dept/school/lab 1", "Author 2 - institution 1", "Author 2 - city 1", "Author 2 - state/prov 1", "Author 2 - country 1", "Author 2 - dept/school/lab 2", "Author 2 - institution 2", "Author 2 - city 2", "Author 2 - state/prov 2", "Author 2 - country 2",
            "Author 3 - id", "Author 3 - prefix", "Author 3 - first", "Author 3 - middle", "Author 3 - last", "Author 3 - suffix", "Author 3 - email", "Author 3 - dept/school/lab 1", "Author 3 - institution 1", "Author 3 - city 1", "Author 3 - state/prov 1", "Author 3 - country 1", "Author 3 - dept/school/lab 2", "Author 3 - institution 2", "Author 3 - city 2", "Author 3 - state/prov 2", "Author 3 - country 2",
            "Author 4 - id", "Author 4 - prefix", "Author 4 - first", "Author 4 - middle", "Author 4 - last", "Author 4 - suffix", "Author 4 - email", "Author 4 - dept/school/lab 1", "Author 4 - institution 1", "Author 4 - city 1", "Author 4 - state/prov 1", "Author 4 - country 1", "Author 4 - dept/school/lab 2", "Author 4 - institution 2", "Author 4 - city 2", "Author 4 - state/prov 2", "Author 4 - country 2",
            "Author 5 - id", "Author 5 - prefix", "Author 5 - first", "Author 5 - middle", "Author 5 - last", "Author 5 - suffix", "Author 5 - email", "Author 5 - dept/school/lab 1", "Author 5 - institution 1", "Author 5 - city 1", "Author 5 - state/prov 1", "Author 5 - country 1", "Author 5 - dept/school/lab 2", "Author 5 - institution 2", "Author 5 - city 2", "Author 5 - state/prov 2", "Author 5 - country 2",
            "Author 6 - id", "Author 6 - prefix", "Author 6 - first", "Author 6 - middle", "Author 6 - last", "Author 6 - suffix", "Author 6 - email", "Author 6 - dept/school/lab 1", "Author 6 - institution 1", "Author 6 - city 1", "Author 6 - state/prov 1", "Author 6 - country 1", "Author 6 - dept/school/lab 2", "Author 6 - institution 2", "Author 6 - city 2", "Author 6 - state/prov 2", "Author 6 - country 2",
            "Author 7 - id", "Author 7 - prefix", "Author 7 - first", "Author 7 - middle", "Author 7 - last", "Author 7 - suffix", "Author 7 - email", "Author 7 - dept/school/lab 1", "Author 7 - institution 1", "Author 7 - city 1", "Author 7 - state/prov 1", "Author 7 - country 1", "Author 7 - dept/school/lab 2", "Author 7 - institution 2", "Author 7 - city 2", "Author 7 - state/prov 2", "Author 7 - country 2",
            "Author 8 - id", "Author 8 - prefix", "Author 8 - first", "Author 8 - middle", "Author 8 - last", "Author 8 - suffix", "Author 8 - email", "Author 8 - dept/school/lab 1", "Author 8 - institution 1", "Author 8 - city 1", "Author 8 - state/prov 1", "Author 8 - country 1", "Author 8 - dept/school/lab 2", "Author 8 - institution 2", "Author 8 - city 2", "Author 8 - state/prov 2", "Author 8 - country 2",
            "Author 9 - id", "Author 9 - prefix", "Author 9 - first", "Author 9 - middle", "Author 9 - last", "Author 9 - suffix", "Author 9 - email", "Author 9 - dept/school/lab 1", "Author 9 - institution 1", "Author 9 - city 1", "Author 9 - state/prov 1", "Author 9 - country 1", "Author 9 - dept/school/lab 2", "Author 9 - institution 2", "Author 9 - city 2", "Author 9 - state/prov 2", "Author 9 - country 2",
            "Author 10 - id", "Author 10 - prefix", "Author 10 - first", "Author 10 - middle", "Author 10 - last", "Author 10 - suffix", "Author 10 - email", "Author 10 - dept/school/lab 1", "Author 10 - institution 1", "Author 10 - city 1", "Author 10 - state/prov 1", "Author 10 - country 1", "Author 10 - dept/school/lab 2", "Author 10 - institution 2", "Author 10 - city 2", "Author 10 - state/prov 2", "Author 10 - country 2",
            "Author 11 - id", "Author 11 - prefix", "Author 11 - first", "Author 11 - middle", "Author 11 - last", "Author 11 - suffix", "Author 11 - email", "Author 11 - dept/school/lab 1", "Author 11 - institution 1", "Author 11 - city 1", "Author 11 - state/prov 1", "Author 11 - country 1", "Author 11 - dept/school/lab 2", "Author 11 - institution 2", "Author 11 - city 2", "Author 11 - state/prov 2", "Author 11 - country 2",
            "Author 12 - id", "Author 12 - prefix", "Author 12 - first", "Author 12 - middle", "Author 12 - last", "Author 12 - suffix", "Author 12 - email", "Author 12 - dept/school/lab 1", "Author 12 - institution 1", "Author 12 - city 1", "Author 12 - state/prov 1", "Author 12 - country 1", "Author 12 - dept/school/lab 2", "Author 12 - institution 2", "Author 12 - city 2", "Author 12 - state/prov 2", "Author 12 - country 2",
            "Author 13 - id", "Author 13 - prefix", "Author 13 - first", "Author 13 - middle", "Author 13 - last", "Author 13 - suffix", "Author 13 - email", "Author 13 - dept/school/lab 1", "Author 13 - institution 1", "Author 13 - city 1", "Author 13 - state/prov 1", "Author 13 - country 1", "Author 13 - dept/school/lab 2", "Author 13 - institution 2", "Author 13 - city 2", "Author 13 - state/prov 2", "Author 13 - country 2",
            "Author 14 - id", "Author 14 - prefix", "Author 14 - first", "Author 14 - middle", "Author 14 - last", "Author 14 - suffix", "Author 14 - email", "Author 14 - dept/school/lab 1", "Author 14 - institution 1", "Author 14 - city 1", "Author 14 - state/prov 1", "Author 14 - country 1", "Author 14 - dept/school/lab 2", "Author 14 - institution 2", "Author 14 - city 2", "Author 14 - state/prov 2", "Author 14 - country 2",
            "Author 15 - id", "Author 15 - prefix", "Author 15 - first", "Author 15 - middle", "Author 15 - last", "Author 15 - suffix", "Author 15 - email", "Author 15 - dept/school/lab 1", "Author 15 - institution 1", "Author 15 - city 1", "Author 15 - state/prov 1", "Author 15 - country 1", "Author 15 - dept/school/lab 2", "Author 15 - institution 2", "Author 15 - city 2", "Author 15 - state/prov 2", "Author 15 - country 2",
            "Author 16 - id", "Author 16 - prefix", "Author 16 - first", "Author 16 - middle", "Author 16 - last", "Author 16 - suffix", "Author 16 - email", "Author 16 - dept/school/lab 1", "Author 16 - institution 1", "Author 16 - city 1", "Author 16 - state/prov 1", "Author 16 - country 1", "Author 16 - dept/school/lab 2", "Author 16 - institution 2", "Author 16 - city 2", "Author 16 - state/prov 2", "Author 16 - country 2",
            "Author 17 - id", "Author 17 - prefix", "Author 17 - first", "Author 17 - middle", "Author 17 - last", "Author 17 - suffix", "Author 17 - email", "Author 17 - dept/school/lab 1", "Author 17 - institution 1", "Author 17 - city 1", "Author 17 - state/prov 1", "Author 17 - country 1", "Author 17 - dept/school/lab 2", "Author 17 - institution 2", "Author 17 - city 2", "Author 17 - state/prov 2", "Author 17 - country 2",
            "Author 18 - id", "Author 18 - prefix", "Author 18 - first", "Author 18 - middle", "Author 18 - last", "Author 18 - suffix", "Author 18 - email", "Author 18 - dept/school/lab 1", "Author 18 - institution 1", "Author 18 - city 1", "Author 18 - state/prov 1", "Author 18 - country 1", "Author 18 - dept/school/lab 2", "Author 18 - institution 2", "Author 18 - city 2", "Author 18 - state/prov 2", "Author 18 - country 2",
            "Author 19 - id", "Author 19 - prefix", "Author 19 - first", "Author 19 - middle", "Author 19 - last", "Author 19 - suffix", "Author 19 - email", "Author 19 - dept/school/lab 1", "Author 19 - institution 1", "Author 19 - city 1", "Author 19 - state/prov 1", "Author 19 - country 1", "Author 19 - dept/school/lab 2", "Author 19 - institution 2", "Author 19 - city 2", "Author 19 - state/prov 2", "Author 19 - country 2",
            "Author 20 - id", "Author 20 - prefix", "Author 20 - first", "Author 20 - middle", "Author 20 - last", "Author 20 - suffix", "Author 20 - email", "Author 20 - dept/school/lab 1", "Author 20 - institution 1", "Author 20 - city 1", "Author 20 - state/prov 1", "Author 20 - country 1", "Author 20 - dept/school/lab 2", "Author 20 - institution 2", "Author 20 - city 2", "Author 20 - state/prov 2", "Author 20 - country 2",
            "Author 21 - id", "Author 21 - prefix", "Author 21 - first", "Author 21 - middle", "Author 21 - last", "Author 21 - suffix", "Author 21 - email", "Author 21 - dept/school/lab 1", "Author 21 - institution 1", "Author 21 - city 1", "Author 21 - state/prov 1", "Author 21 - country 1", "Author 21 - dept/school/lab 2", "Author 21 - institution 2", "Author 21 - city 2", "Author 21 - state/prov 2", "Author 21 - country 2",
            "Author 22 - id", "Author 22 - prefix", "Author 22 - first", "Author 22 - middle", "Author 22 - last", "Author 22 - suffix", "Author 22 - email", "Author 22 - dept/school/lab 1", "Author 22 - institution 1", "Author 22 - city 1", "Author 22 - state/prov 1", "Author 22 - country 1", "Author 22 - dept/school/lab 2", "Author 22 - institution 2", "Author 22 - city 2", "Author 22 - state/prov 2", "Author 22 - country 2",
            "Author 23 - id", "Author 23 - prefix", "Author 23 - first", "Author 23 - middle", "Author 23 - last", "Author 23 - suffix", "Author 23 - email", "Author 23 - dept/school/lab 1", "Author 23 - institution 1", "Author 23 - city 1", "Author 23 - state/prov 1", "Author 23 - country 1", "Author 23 - dept/school/lab 2", "Author 23 - institution 2", "Author 23 - city 2", "Author 23 - state/prov 2", "Author 23 - country 2",
            "Author 24 - id", "Author 24 - prefix", "Author 24 - first", "Author 24 - middle", "Author 24 - last", "Author 24 - suffix", "Author 24 - email", "Author 24 - dept/school/lab 1", "Author 24 - institution 1", "Author 24 - city 1", "Author 24 - state/prov 1", "Author 24 - country 1", "Author 24 - dept/school/lab 2", "Author 24 - institution 2", "Author 24 - city 2", "Author 24 - state/prov 2", "Author 24 - country 2",
            "ACM Author Affiliations", "ACM Author Emails, excluding contact email"
        ]
        for row in data:
            for key in keys_to_be_deleted:
                del row[key]

    return data


data_1 = load_data_1(input_1_path)
