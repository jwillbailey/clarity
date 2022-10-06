import argparse
import glob
import json
import logging
from pathlib import Path

import pandas as pd
from pandas_profiling import ProfileReport

logging.basicConfig(level=logging.INFO, filename="logs/score_listenhome.log")


def report_scores(responses):
    """Report scores for each response"""
    n_hits_words = sum(r["hits_words"] for r in responses)
    n_words = sum(r["n_words"] for r in responses)
    words_correct = n_hits_words / n_words * 100
    n_hits_phonemes = sum(r["hits_phonemes"] for r in responses)
    n_phonemes = sum(r["n_phonemes"] for r in responses)
    phonemes_correct = n_hits_phonemes / n_phonemes * 100
    return words_correct, phonemes_correct


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", type=str)
    parser.add_argument("save_dir", type=str)
    args = parser.parse_args()

    all_responses = []
    for filename in glob.glob(args.input_files):
        file = Path(filename).name
        responses = json.load(open(filename, "r", encoding="utf-8"))
        all_responses.extend(responses)
        words_correct, phonemes_correct = report_scores(responses)
        print(f"{file} {words_correct:3.1f}, {phonemes_correct:3.1f}")

    df = pd.DataFrame(all_responses)
    profile = ProfileReport(df, title="Pandas Profiling Report")
    profile.to_file(args.save_dir + "/scores.html")

    words_correct, phonemes_correct = report_scores(all_responses)
    print(f"Overall: {words_correct:3.1f}, {phonemes_correct:3.1f}")


if __name__ == "__main__":
    main()
