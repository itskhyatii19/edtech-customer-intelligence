import pandas as pd
import os

def load_data():
    # Get project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    users = pd.read_csv(os.path.join(project_root, "data/junyi/raw/Info_UserData.csv"))
    logs = pd.read_csv(os.path.join(project_root, "data/junyi/raw/Log_Problem.csv"), nrows=500000)
    return users, logs


def create_engagement(logs):
    engagement = logs.groupby("uuid").size().reset_index(name="activity_count")
    engagement["engagement_score"] = (
        engagement["activity_count"] / engagement["activity_count"].max()
    )
    return engagement


def create_inactivity(logs):
    logs["timestamp_TW"] = pd.to_datetime(logs["timestamp_TW"])

    last_activity = logs.groupby("uuid")["timestamp_TW"].max().reset_index()

    today = logs["timestamp_TW"].max()

    last_activity["inactive_days"] = (
        today - last_activity["timestamp_TW"]
    ).dt.days

    return last_activity[["uuid", "inactive_days"]]


def merge_features(users, engagement, inactivity):
    df = users.merge(engagement, on="uuid", how="left")
    df = df.merge(inactivity, on="uuid", how="left")

    df["activity_count"] = df["activity_count"].fillna(0)
    df["engagement_score"] = df["engagement_score"].fillna(0)
    df["inactive_days"] = df["inactive_days"].fillna(999)
    df["gender"] = df["gender"].fillna("unknown")
    df["inactive_days"] = df["inactive_days"].clip(upper=365)

    return df


def compute_churn(df):
    eng_threshold = df["engagement_score"].quantile(0.3)
    inactive_threshold = df["inactive_days"].quantile(0.7)

    df["churn_risk"] = "low"

    df.loc[
        (df["engagement_score"] < eng_threshold) |
        (df["inactive_days"] > inactive_threshold),
        "churn_risk"
    ] = "high"
    df["activity_count"] = df["activity_count"].astype(int)
    df["inactive_days"] = df["inactive_days"].astype(int)
    return df


def segment_users(df):
    def segment(score):
        if score > 0.7:
            return "highly_active"
        elif score > 0.3:
            return "moderate"
        else:
            return "low_active"

    df["user_segment"] = df["engagement_score"].apply(segment)
    return df


def build_features():
    users, logs = load_data()
    engagement = create_engagement(logs)
    inactivity = create_inactivity(logs)

    df = merge_features(users, engagement, inactivity)
    df = compute_churn(df)
    df = segment_users(df)

    return df

