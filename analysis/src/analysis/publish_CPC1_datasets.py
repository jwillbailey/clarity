import argparse
import json
import logging
import random
from random import Random

import pandas as pd

logging.basicConfig(level=logging.INFO, filename="logs/split_CPC1_datasets.log")


N_LISTENERS_TEST = 5
N_SCENES_TEST = 200

systems_train = ["E001", "E003", "E005", "E007", "E009", "E010", "E013", "E019", "E021"]
systems_test = ["E018"]  # Chosen by hand as generating the biggest spread of performance

# 22 listeners out of 27
# Listener 227 in an outlier
listeners_all = [
    "L0200",
    "L0201",
    "L0202",
    "L0206",
    "L0203",
    "L0209",
    "L0212",
    "L0215",
    "L0216",
    "L0217",
    "L0218",
    "L0219",
    "L0220",
    "L0221",
    "L0222",
    "L0224",
    "L0225",
    "L0227",
    "L0229",
    "L0231",
    "L0235",
    "L0236",
    "L0239",
    "L0240",
    "L0241",
    "L0242",
    "L0243",
    "L0244",
    "L0247",
    "L0248",
    "L0249",
    "L0251",
    "L0252",
    "L0254",
]
# Pick 5

# # This listener is an outlier with particular poor performance
# # Not suitable for inclusion in the test set?
# listeners_outliers = ["L0227"]

# 'randomly' selected to but capture the spread in average performance
listeners_test = ["L0202", "L0203", "L0220", "L0235", "L0241"]

# The Following listeners are NH controls. Not to be included
listeners_nh = ["L0244", "L0247", "L0248", "L0249", "L0251", "L0252", "L0254"]


"""
 ['exp', 'stimulus', 'md5', 'prompt', 'scene', 'hypothesis', 'transcript',
       'n_words', 'hits_words', 'n_phonemes', 'hits_phonemes', 'listener',
       'system', 'audiogram', 'room', 'hrirfilename', 'target',
       'listener_data', 'interferer', 'azimuth_target_listener',
       'azimuth_interferer_listener', 'dataset', 'pre_samples', 'post_samples',
       'SNR', 'mbstoi', 'words_corr', 'phonemes_corr']
"""


publish_keys = [
    "prompt",
    "scene",
    "n_words",
    "hits_words",
    "listener",
    "system",
    "words_corr",
    "scored_form",
    "volume",
]


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("master_file", type=str)
    parser.add_argument("save_file_stem", type=str)
    args = parser.parse_args()

    # Training listeners are those not in test set or control set
    listeners_train = [
        l for l in listeners_all if l not in listeners_test and l not in listeners_nh
    ]

    listeners_used = listeners_train + listeners_test

    # Read in the complete master file
    df_raw = pd.DataFrame(json.load(open(args.master_file, "r")))

    # Removes the 'warmup' stimuli from all tests
    df_raw = df_raw[df_raw.stimulus > 3]

    # Retain only the listeners used in train or test
    df = df_raw[df_raw["listener"].isin(listeners_used)]

    # Listener ID replaced with audiogram ID
    # i.e. Listener is the Listener ID on listen@home which is meant
    # to match the audiogram. Except L0208 was registered at L0203 (doh!)
    # because they were posted the wrong tablet.

    df["listener"] = df["audiogram"]

    # Retain only a subset of the keys
    df = df[publish_keys].copy()

    # Make the unique signal identifier from scene, listener and system
    df["signal"] = df["scene"] + "_" + df["listener"] + "_" + df["system"]

    # Some field renaming to make things clearer for entrants
    df = df.rename(
        {"scored_form": "response", "words_corr": "correctness", "hits_words": "hits"}, axis=1
    )

    # Convert prompt and response to lowercase.
    df.prompt = df.prompt.str.lower()
    df.response = df.response.str.lower()

    # Split the scenes into train and test
    # scenes = list(set(df["scene"]))  # This version is not deterministic! Use unique() instead.
    scenes = df["scene"].unique()
    Random(0).shuffle(scenes)  # Notice the fixed seed for this invocation of shuffle
    scenes_train = sorted(scenes[N_SCENES_TEST:])

    # Remove '#' and '!' notations from response
    df.response = df.response.str.replace("#", "")
    df.response = df.response.str.replace("!", "")

    # Remove any responses that still contain some unresolved tag
    df = df[~df.response.str.contains("\[")]

    # Split the scenes into train and test

    # Set 000 - pure train set
    df_set000 = df[
        df["scene"].isin(scenes_train)
        & df["listener"].isin(listeners_train)
        & df["system"].isin(systems_train)
    ]

    # Factions that overlap with train set in different ways
    df_set001 = df[
        df["scene"].isin(scenes_train)
        & df["listener"].isin(listeners_train)
        & ~df["system"].isin(systems_train)
    ]
    df_set010 = df[
        df["scene"].isin(scenes_train)
        & ~df["listener"].isin(listeners_train)
        & df["system"].isin(systems_train)
    ]
    df_set011 = df[
        df["scene"].isin(scenes_train)
        & ~df["listener"].isin(listeners_train)
        & ~df["system"].isin(systems_train)
    ]
    df_set100 = df[
        ~df["scene"].isin(scenes_train)
        & df["listener"].isin(listeners_train)
        & df["system"].isin(systems_train)
    ]
    df_set101 = df[
        ~df["scene"].isin(scenes_train)
        & df["listener"].isin(listeners_train)
        & ~df["system"].isin(systems_train)
    ]
    df_set110 = df[
        ~df["scene"].isin(scenes_train)
        & ~df["listener"].isin(listeners_train)
        & df["system"].isin(systems_train)
    ]
    df_set111 = df[
        ~df["scene"].isin(scenes_train)
        & ~df["listener"].isin(listeners_train)
        & ~df["system"].isin(systems_train)
    ]

    # Make the published sets from the above factions
    df_train = df_set000
    df_train_extended = pd.concat((df_set000, df_set001, df_set010, df_set011))
    df_test_all = pd.concat((df_set100, df_set101, df_set110, df_set111))
    df_test_indep = pd.concat((df_set101, df_set110, df_set111))

    print(len(df_train), len(df_train_extended), len(df_test_all), len(df_test_indep))

    # Save the sets.
    df_train.to_json(f"{args.save_file_stem}.train_indep.json", orient="records", indent=2)
    df_train_extended.to_json(f"{args.save_file_stem}.train.json", orient="records", indent=2)
    df_test_all.to_json(f"{args.save_file_stem}.test.json", orient="records", indent=2)
    df_test_indep.to_json(f"{args.save_file_stem}.test_indep.json", orient="records", indent=2)


if __name__ == "__main__":
    main()
