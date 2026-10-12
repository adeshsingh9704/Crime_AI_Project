import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import LEGAL_CASES_FILE


cases = pd.read_csv(
    LEGAL_CASES_FILE
)

cases["case_text"] = (
    cases["case_text"]
    .fillna("")
    .astype(str)
)


vectorizer = TfidfVectorizer(
    stop_words="english"
)

X = vectorizer.fit_transform(
    cases["case_text"]
)


def suggest_lawyer(user_case):

    user_case = str(
        user_case
    ).strip()

    if not user_case:

        return {
            "status": "ERROR",
            "lawyer": "",
            "fee": "",
            "message": (
                "Please enter case details."
            )
        }

    query = vectorizer.transform([
        user_case
    ])

    similarity = cosine_similarity(
        query,
        X
    )

    index = similarity.argmax()

    row = cases.iloc[index]

    return {
        "status": "OK",
        "lawyer": str(row["lawyer"]),
        "fee": str(row["fee"]),
        "historical_win_rate": str(
            row["win_rate"]
        ),
        "similarity": round(
            float(similarity[0][index]),
            3
        ),
        "message": (
            "This is a similarity-based "
            "demo using the supplied legal "
            "case dataset. Historical win "
            "rate is not a prediction of "
            "case outcome."
        )
    }