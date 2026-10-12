import pandas as pd
from sklearn.cluster import DBSCAN

from config import CRIME_DATA_FILE


# ============================================================
# LOAD DATA
# ============================================================

def load_crime_data():
    """Load crime location data from CSV."""

    df = pd.read_csv(CRIME_DATA_FILE)

    required_columns = {"lat", "lon", "crime_type"}

    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(
            f"Missing required columns in crime_data.csv: {missing}"
        )

    return df.dropna(
        subset=["lat", "lon"]
    ).copy()


# ============================================================
# DBSCAN HOTSPOT DETECTION
# ============================================================

def detect_hotspots(
    df=None,
    eps=0.02,
    min_samples=2
):
    """
    Detect geographical clusters using DBSCAN.

    cluster = -1 means the point is not assigned
    to a detected cluster.
    """

    if df is None:
        df = load_crime_data()

    if len(df) == 0:
        df["cluster"] = -1
        return df

    coordinates = df[
        ["lat", "lon"]
    ].values

    model = DBSCAN(
        eps=eps,
        min_samples=min_samples
    )

    df["cluster"] = model.fit_predict(
        coordinates
    )

    return df


# ============================================================
# GET HOTSPOTS
# ============================================================

def get_hotspots():
    """Return detected hotspot clusters."""

    df = load_crime_data()

    clustered = detect_hotspots(df)

    hotspots = []

    valid_clusters = [
        cluster
        for cluster in sorted(
            clustered["cluster"].unique()
        )
        if cluster != -1
    ]

    for cluster_id in valid_clusters:

        cluster_data = clustered[
            clustered["cluster"] == cluster_id
        ]

        latitude = float(
            cluster_data["lat"].mean()
        )

        longitude = float(
            cluster_data["lon"].mean()
        )

        crime_counts = (
            cluster_data["crime_type"]
            .value_counts()
            .to_dict()
        )

        hotspots.append({
            "cluster_id": int(cluster_id),
            "latitude": latitude,
            "longitude": longitude,
            "crime_count": int(
                len(cluster_data)
            ),
            "crime_types": crime_counts
        })

    return hotspots


# ============================================================
# LOCATION CHECK
# ============================================================

def check_location(latitude, longitude):
    """
    Compare a supplied location with historical
    crime clusters.

    This is a proximity analysis of the dataset.
    It is not a prediction of future crime.
    """

    hotspots = get_hotspots()

    if not hotspots:

        return {
            "status": "No hotspot data available",
            "risk": "Unknown",
            "nearest_hotspot": None,
            "distance_degrees": None
        }

    def distance(hotspot):

        return (
            (
                hotspot["latitude"]
                - latitude
            ) ** 2
            +
            (
                hotspot["longitude"]
                - longitude
            ) ** 2
        ) ** 0.5

    nearest = min(
        hotspots,
        key=distance
    )

    nearest_distance = distance(
        nearest
    )

    if nearest_distance <= 0.005:

        status = "Near historical hotspot"
        risk = "High"

    elif nearest_distance <= 0.015:

        status = (
            "Relatively near historical hotspot"
        )
        risk = "Medium"

    else:

        status = "Away from detected hotspot"
        risk = "Low"

    return {
        "status": status,
        "risk": risk,
        "nearest_hotspot": nearest,
        "distance_degrees": round(
            nearest_distance,
            6
        )
    }


# ============================================================
# NEAREST HOTSPOT
# ============================================================

def get_nearest_hotspot(
    latitude,
    longitude
):
    """Find the nearest hotspot."""

    hotspots = get_hotspots()

    if not hotspots:
        return None

    def distance(hotspot):

        return (
            (
                hotspot["latitude"]
                - latitude
            ) ** 2
            +
            (
                hotspot["longitude"]
                - longitude
            ) ** 2
        ) ** 0.5

    nearest = min(
        hotspots,
        key=distance
    )

    result = nearest.copy()

    result["distance_degrees"] = round(
        distance(nearest),
        6
    )

    return result


# ============================================================
# STATISTICS
# ============================================================

def get_statistics():
    """
    Return statistics used by the dashboard.
    """

    df = load_crime_data()

    clustered = detect_hotspots(df)

    total_records = len(
        clustered
    )

    hotspot_records = clustered[
        clustered["cluster"] != -1
    ]

    cluster_count = len(
        set(
            clustered["cluster"]
        ) - {-1}
    )

    crime_distribution = (
        df["crime_type"]
        .value_counts()
        .to_dict()
    )

    return {
        "total_records": int(
            total_records
        ),

        "hotspot_count": int(
            cluster_count
        ),

        "records_in_hotspots": int(
            len(hotspot_records)
        ),

        "crime_distribution":
            crime_distribution
    }


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def get_hotspot_summary():
    """
    Compatibility wrapper.

    Some versions of app.py use
    get_hotspot_summary() instead of
    get_statistics().
    """

    statistics = get_statistics()

    return {
        "total_records":
            statistics["total_records"],

        "hotspot_count":
            statistics["hotspot_count"],

        "records_in_hotspots":
            statistics["records_in_hotspots"]
    }