from train_classifier import train_random_forest, FEATURES
from shape_data import windowify, shape_json
from collections import deque
import joblib
import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier

_WINDOW_LENGTH = 30
_MODEL_PATH = "trained_model_random_forest.joblib"
_TRAINING_DATA_PATH = "training_data"
_loaded_model = None


data_queue = deque(maxlen=_WINDOW_LENGTH)


def train_model(show_confusion: bool, persist: bool) -> bool:
    global _loaded_model
    persist_path = persist and _MODEL_PATH or None
    _loaded_model = train_random_forest(_TRAINING_DATA_PATH, persist_path, show_confusion)
    return True


def load_model() -> bool:
    global _loaded_model
    _loaded_model = joblib.load(_MODEL_PATH)
    return True


def push_data(data) -> bool:
    data_queue.append(data)
    return True


def is_model_loaded() -> bool:
    global _loaded_model
    return bool(_loaded_model)


def estimate_current_state() -> tuple[str, float]:
    global _loaded_model
    window_size = len(data_queue)
    if window_size <= 0:
        return ("not present", 0)

    windows = windowify(shape_json(list(data_queue)), window_size)
    current_window_dict = windows[0]
    model_input_list = [current_window_dict[f] for f in FEATURES]
    model_input = np.array(model_input_list).reshape(1, -1)

    prediction = _loaded_model.predict(model_input)[0]
    probabilities = _loaded_model.predict_proba(model_input)
    confidence = np.max(probabilities) * (window_size / _WINDOW_LENGTH)

    return (str(prediction), float(confidence))
