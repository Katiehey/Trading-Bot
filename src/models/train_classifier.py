#✅ 1. Create a model training script using RandomForestClassifier with time series cross-validation.
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score


FEATURES = [
    "EMA_12",
    "EMA_26",
    "SMA_50",
    "SMA_200",
    "MACD_12_26_9",
    "MACDh_12_26_9",
    "MACDs_12_26_9",
    "RSI_14",
    "ATRr_14",
    "BBL_20_2.0_2.0",
    "BBM_20_2.0_2.0",
    "BBU_20_2.0_2.0",
    "BBB_20_2.0_2.0",
    "BBP_20_2.0_2.0",
    "EMA_20",
    "OBV",
    "hour",
    "day_of_week",
    "is_weekend"
]


def train_model(df: pd.DataFrame):
    X = df[FEATURES]
    y = df["target"]

    tscv = TimeSeriesSplit(n_splits=5)

    scores = []
    for train_idx, test_idx in tscv.split(X):
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=5,
            random_state=42
        )
        model.fit(X.iloc[train_idx], y.iloc[train_idx])

        preds = model.predict(X.iloc[test_idx])
        acc = accuracy_score(y.iloc[test_idx], preds)
        scores.append(acc)

    print("CV Accuracy:", sum(scores) / len(scores))

    model.fit(X, y)
    return model
