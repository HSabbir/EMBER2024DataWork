"""
Train a LightGBM classifier on vectorized EMBER2024 features.

The following LightGBM config files were used for training the benchmark models:
 - Benign/malicious detection: lgbm_config.json
 - Malware family classification: lgbm_config_family.json
 - All other classification tasks: lgbm_config_tag.json
"""

import os
import json
import thrember
import argparse
import lightgbm as lgb
from sklearn.model_selection import train_test_split


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", type=str,
                        help="Path to the directory containing the EMBER2024 dataset.")
    parser.add_argument("model_path", type=str,
                        help="Path to save the trained model.")
    parser.add_argument("--config-file", type=str, default="lgbm_config.json",
                        help="Path to LightGBM config file.")
    args = parser.parse_args()

    # Validate data directory and config file
    if not os.path.isdir(args.data_dir):
        raise ValueError("Not a directory: {}".format(args.data_dir))
    if not os.path.isfile(args.config_file):
        raise ValueError("Not a file: {}".format(args.config_file))

    # Parse LightGBM config file
    fit_params = json.load(open(args.config_file, "r"))

    # Load data and train model
    model = thrember.train_model(args.data_dir, params=fit_params)

    # Save model
    model.save_model(args.model_path, num_iteration=model.best_iteration)
