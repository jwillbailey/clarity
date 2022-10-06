"""Copy transcription

Takes a set of transcriptions and generates a new set in the published format.
A respnonse will contain a single transcription field with just the text.
Information about transcribers and transcription datestamps is stripped out.add()

By default the track labeled '00' is used as the source of the transcription.

The integrity of the complete transcription set is checked first and if any
response is missing a transcription then the entire set is rejected and the 
program exits without writing any new files.
"""

import argparse
import glob
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, filename="logs/publish_transcription.log")


def check_transcript(transcript, transcriber_label):
    """Check the integrity of the transcription

    Args:
        transcript (dict): [description]
        transcriber_label (str): [description]

    Returns:
        [type]: [description]
    """
    for response in transcript:
        if "transcripts" not in response or transcriber_label not in response["transcripts"]:
            return False
    return True


def publish_one_transcript(transcript_from, transcriber_label="00"):
    """[summary]

    Args:
        transcript_from ([type]): [description]
        transcriber_label (str, optional): [description]. Defaults to "00".

    Returns:
        [type]: [description]
    """
    transcript_new = transcript_from.copy()
    for response in transcript_new:
        transcripts = response["transcripts"]
        response["transcript"] = transcripts[transcriber_label]["transcript"]
        del response["transcripts"]
    return transcript_new


def publish_transcription(input_files, save_dir, label):
    files_to_process = glob.glob(input_files)
    filenames = [Path(file).name for file in files_to_process]
    transcripts_to_process = [json.load(open(f, "r")) for f in files_to_process]

    errored_transcripts = [
        transcript
        for transcript in transcripts_to_process
        if not check_transcript(transcript, label)
    ]

    if len(errored_transcripts) > 0:
        logging.error(f"{len(errored_transcripts)} transcripts files with missing transcriptions.")
        print("Transcripts with errors. Check log.")
        return

    for filename, transcript in zip(filenames, transcripts_to_process):
        published_transcript = publish_one_transcript(transcript, label)
        with open(save_dir + "/" + filename, "w") as f:
            json.dump(published_transcript, f, indent=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--label", type=str, default="00", help="Label of the transcription track to publish"
    )
    parser.add_argument("input_files", type=str)
    parser.add_argument("save_dir", type=str)
    args = parser.parse_args()

    publish_transcription(args.input_files, args.save_dir, args.label)


if __name__ == "__main__":
    main()

# python3 publish_transcription.py data/transcriptions/*.json data/transcriptions.published
