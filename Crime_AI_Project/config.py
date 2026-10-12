import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(BASE_DIR, "dataset")

CRIME_DATA_FILE = os.path.join(
    DATASET_DIR,
    "crime_data.csv"
)

CRIME_RECORDS_FILE = os.path.join(
    DATASET_DIR,
    "crime_records.csv"
)

LEGAL_CASES_FILE = os.path.join(
    DATASET_DIR,
    "legal_cases.csv"
)

FACES_DIR = os.path.join(
    DATASET_DIR,
    "faces"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "reports"
)