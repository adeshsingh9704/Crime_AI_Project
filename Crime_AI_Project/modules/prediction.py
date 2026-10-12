import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from config import CRIME_DATA_FILE


data = pd.read_csv(CRIME_DATA_FILE)

data["lat"] = pd.to_numeric(
    data["lat"],
    errors="coerce"
)

data["lon"] = pd.to_numeric(
    data["lon"],
    errors="coerce"
)

data = data.dropna(
    subset=[
        "lat",
        "lon",
        "crime_type"
    ]
)


FEATURES = [
    "lat",
    "lon"
]


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


model.fit(
    data[FEATURES],
    data["crime_type"]
)


def predict_crime(lat, lon):

    prediction = model.predict([
        [lat, lon]
    ])[0]

    probabilities = model.predict_proba([
        [lat, lon]
    ])[0]

    classes = model.classes_

    probability_data = {}

    for crime, probability in zip(
        classes,
        probabilities
    ):

        probability_data[str(crime)] = round(
            float(probability) * 100,
            2
        )

    return {
        "status": "OK",
        "prediction": str(prediction),
        "probabilities": probability_data,
        "note": (
            "Demonstration model based on "
            "the available historical dataset."
        )
    }