import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


FEATURES = ['avg_distance', 'stdev_distance', 'num_motion', 'num_sound', 'motion_min_sec', 'sound_min_sec']


def timedelta_str_to_seconds(td_str):
    h, m, s_micro = map(float, td_str.split(':'))
    return h * 3600 + m * 60 + s_micro


def load_and_prepare_data(paths):
    X = []
    Y = []

    for (path, label) in paths:
        print(f"Loading data from: {path}")
        with open(path, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        df['motion_min_sec'] = df['motion_min'].apply(timedelta_str_to_seconds)
        df['sound_min_sec'] = df['sound_min'].apply(timedelta_str_to_seconds)

        X.extend(df[FEATURES].values)
        Y.extend([label for _ in range(len(df))])

    X = np.array(X)
    Y = np.array(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.3, random_state=42, stratify=Y
    )

    return X_train, X_test, Y_train, Y_test


X_train, X_test, Y_train, Y_test = load_and_prepare_data([
    ("training_data/data_present.json", "present"),
    ("training_data/data_present_v2.json", "present"),
    ("training_data/data_not_present.json", "not present")
])


if X_train is not None:
    print(f"\nData successfully loaded and split:")
    print(f"Training set size: {len(X_train)} samples")
    print(f"Testing set size: {len(X_test)} samples")
    print(f"Number of features: {X_train.shape[1]}")

    # Initialize and Train the Random Forest Classifier
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=8, 
        random_state=42,
        class_weight='balanced'
    )

    print("\n--- Training Random Forest Model ---")
    clf.fit(X_train, Y_train)
    print("Training complete.")

    accuracy = clf.score(X_test, Y_test)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}")