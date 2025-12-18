import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib

FEATURES = ['avg_distance', 'stdev_distance', 'num_motion', 'num_sound', 'motion_min', 'sound_min']


def load_and_prepare_data(paths):
    X = []
    Y = []

    for (path, label) in paths:
        print(f"Loading data from: {path}")
        with open(path, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        X.extend(df[FEATURES].values)
        Y.extend([label for _ in range(len(df))])

    X = np.array(X)
    Y = np.array(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.3, random_state=42, stratify=Y
    )

    return X_train, X_test, Y_train, Y_test


def find_training_data(root_path):
    training_data = []
    for path in Path(root_path).rglob("*.json"):
        if path.is_file():
            label = path.parent.name
            file = str(path)
            training_data.append((file, label))
    return training_data


def train_random_forest(training_data_root_path, model_path, show_confusion_matrix):
    training_data = find_training_data(training_data_root_path)
    X_train, X_test, Y_train, Y_test = load_and_prepare_data(training_data)

    print(f"\nData successfully loaded and split:")
    print(f"Training set size: {len(X_train)} samples")
    print(f"Testing set size: {len(X_test)} samples")
    print(f"Number of features: {X_train.shape[1]}")

    # Initialize and Train the Random Forest Classifier
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10, 
        random_state=42,
        class_weight='balanced'
    )

    print("\n--- Training Random Forest Model ---")
    clf.fit(X_train, Y_train)
    print("Training complete.")
    accuracy = clf.score(X_test, Y_test)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}")

    if model_path:
        print(f"Writing model data to '{model_path}'")
        joblib.dump(clf, model_path)

    if show_confusion_matrix:
        print("\nGenerating Confusion Matrix...")
        fig, ax = plt.subplots(figsize=(10, 8))
        cmd = ConfusionMatrixDisplay.from_estimator(
            clf, 
            X_test, 
            Y_test, 
            display_labels=clf.classes_,
            cmap='Blues',
            xticks_rotation=45,
            ax=ax
        )
        plt.title('Random Forest Confusion Matrix')
        plt.tight_layout()
        plt.show() # This will pop up the window with the graph

    return clf
