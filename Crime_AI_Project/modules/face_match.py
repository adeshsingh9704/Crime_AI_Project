import os
import cv2
import pandas as pd

from config import (
    CRIME_RECORDS_FILE,
    FACES_DIR
)


# ---------------------------------------------------------
# LOAD CRIMINAL RECORDS
# ---------------------------------------------------------

records = pd.read_csv(CRIME_RECORDS_FILE)


# Lower score = more visually similar
# This is a demo threshold and should be tested with your images.
MATCH_THRESHOLD = 35


# ---------------------------------------------------------
# IMAGE COMPARISON
# ---------------------------------------------------------

def compare_images(img1, img2):

    # Resize both images to the same size
    img1 = cv2.resize(img1, (200, 200))
    img2 = cv2.resize(img2, (200, 200))

    # Convert to grayscale
    gray1 = cv2.cvtColor(
        img1,
        cv2.COLOR_BGR2GRAY
    )

    gray2 = cv2.cvtColor(
        img2,
        cv2.COLOR_BGR2GRAY
    )

    # Reduce small lighting/noise differences
    gray1 = cv2.GaussianBlur(
        gray1,
        (5, 5),
        0
    )

    gray2 = cv2.GaussianBlur(
        gray2,
        (5, 5),
        0
    )

    # Calculate pixel difference
    difference = cv2.absdiff(
        gray1,
        gray2
    )

    score = float(
        difference.mean()
    )

    return score


# ---------------------------------------------------------
# COMPARE UPLOADED IMAGE
# ---------------------------------------------------------

def compare_uploaded_image(upload_path):

    # Read uploaded image
    uploaded = cv2.imread(
        upload_path
    )

    if uploaded is None:

        return {
            "status": "ERROR",
            "matched": False,
            "message": "Could not read image."
        }


    best_score = float("inf")
    best_record = None


    # -----------------------------------------------------
    # Compare uploaded image with all stored records
    # -----------------------------------------------------

    for _, row in records.iterrows():

        face_id = str(
            row["face_id"]
        ).strip()

        reference_path = os.path.join(
            FACES_DIR,
            face_id
        )


        # Reference image doesn't exist
        if not os.path.exists(
            reference_path
        ):
            continue


        reference = cv2.imread(
            reference_path
        )


        # Reference image cannot be read
        if reference is None:
            continue


        # Compare images
        score = compare_images(
            uploaded,
            reference
        )


        # Keep the closest match
        if score < best_score:

            best_score = score
            best_record = row


    # -----------------------------------------------------
    # No reference image found
    # -----------------------------------------------------

    if best_record is None:

        return {
            "status": "NO_REFERENCE",
            "matched": False,
            "message": (
                "No reference images were found "
                "in the demo dataset."
            )
        }


    # Round score
    best_score = round(
        float(best_score),
        2
    )


    # -----------------------------------------------------
    # MATCH FOUND
    # -----------------------------------------------------

    if best_score <= MATCH_THRESHOLD:

        return {

            "status": "MATCH_FOUND",

            "matched": True,


            # -----------------------------
            # Image information
            # -----------------------------

            "reference_id": str(
                best_record["face_id"]
            ),

            "similarity_score": best_score,


            # -----------------------------
            # Criminal record information
            # -----------------------------

            "fake_id": str(
                best_record["fake_id"]
            ),

            "name": str(
                best_record["name"]
            ),

            "crime": str(
                best_record["crime"]
            ),

            "ipc_section": str(
                best_record["ipc_section"]
            ),

            "verdict": str(
                best_record["verdict"]
            ),


            # -----------------------------
            # Message
            # -----------------------------

            "message": (
                "A sufficiently similar image "
                "was found in the demo dataset. "
                "The record below is associated "
                "with the matched demo image. "
                "This result does not establish identity."
            )
        }


    # -----------------------------------------------------
    # NO MATCH
    # -----------------------------------------------------

    return {

        "status": "NO_MATCH",

        "matched": False,

        "reference_id": None,

        "similarity_score": best_score,

        "message": (
            "No sufficiently similar image "
            "was found in the demo dataset."
        )
    }