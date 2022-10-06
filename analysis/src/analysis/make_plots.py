import argparse
import json
import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logging.basicConfig(level=logging.INFO, filename="logs/make_plots.log")


def make_plots(df, save_dir):

    # Scatter plot of MBSTOI and SNR - not very pretty
    plt.scatter(df["SNR"], df["mbstoi"])
    plt.savefig(save_dir + "/snr_by_mbstoi.png")
    plt.close()

    # System performance distribution - box plot
    fig, ax = plt.subplots(figsize=(14, 6))
    df.groupby(["system"]).boxplot(column=["words_corr"], ax=ax, layout=(1, 10))
    plt.savefig(save_dir + "/system_boxplot.png")

    # Listener performace distribution - box plot
    fig, ax = plt.subplots(figsize=(14, 10))
    df.groupby(["listener"]).boxplot(column=["words_corr"], ax=ax, layout=(2, 18))
    plt.savefig(save_dir + "/listener_boxplot.png")

    # Performace against System and SNR bar plot
    fig, ax = plt.subplots(figsize=(14, 10))
    df_system_snr = df.groupby(["system", "SNR"]).mean().reset_index()
    ax = sns.barplot(x="system", hue="SNR", y="words_corr", data=df_system_snr)
    ax.figure.set_size_inches(14, 10)
    ax.figure.savefig(save_dir + "/correctness_by_snr.png")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("save_dir", type=str)
    args = parser.parse_args()

    df = pd.DataFrame(json.load(open(args.input_file, "r")))

    make_plots(df, args.save_dir)


if __name__ == "__main__":
    main()
