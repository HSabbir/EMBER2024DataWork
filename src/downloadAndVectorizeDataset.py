
import os
import lightgbm as lgb
import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
import thrember

# 1. Setup paths
DATA_DIR = "Your Data Directory"

if __name__ == '__main__':
    thrember.download_dataset(DATA_DIR)

    thrember.create_vectorized_features(DATA_DIR)

    X_train, y_train = thrember.read_vectorized_features(DATA_DIR, subset="train")
    X_test, y_test = thrember.read_vectorized_features(DATA_DIR, subset="test")
    X_challenge, y_challenge = thrember.read_vectorized_features(DATA_DIR, subset="challenge")


    print(f"Train Shape: {X_train.shape}")
    print(f"Test Shape: {X_test.shape}")
    print(f"Challenge Shape: {X_challenge.shape}")

