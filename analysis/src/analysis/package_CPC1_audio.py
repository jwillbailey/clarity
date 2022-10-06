import argparse
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

logging.basicConfig(level=logging.INFO, filename="logs/package_CPC1_audio.log")


def make_infilename(metadata):
    ext = "HA-output"
    inputfile = f"CEC1_{metadata['system']}/{metadata['scene']}_{metadata['listener']}_{ext}.wav"
    return inputfile


def make_outfilename(metadata):
    return f"{metadata['scene']}_{metadata['listener']}_{metadata['system']}.wav"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Strict mode")
    parser.add_argument("audio_in", type=str)
    parser.add_argument(
        "dataset_json", type=str, help="json file where dataset filenams are stored"
    )
    parser.add_argument("output_tar_file", type=str, help="name of the destination tar file")
    parser.add_argument("dataset_name", type=str)

    args = parser.parse_args()

    dataset = json.load(open(args.dataset_json, "r"))

    temp_dir = tempfile.TemporaryDirectory()
    out_root = "CPC1/audio/" + args.dataset_name
    os.makedirs(temp_dir.name + "/" + out_root)

    # Make all input and output filenames
    infiles = [args.audio_in + "/" + make_infilename(sample) for sample in dataset]
    outfiles = [f"{temp_dir.name}/{out_root}/{make_outfilename(sample)}" for sample in dataset]

    # Check existance of all input files
    infiles_exist = [Path(f).exists() for f in infiles]

    # Log any missing input files
    for infile, outfile, exists in zip(infiles, outfiles, infiles_exist):
        if not exists:
            logging.warning(f"{infile} does not exist")

    # If running strict mode then quit if any input files are missing
    if args.strict and not all(infiles_exist):
        raise FileNotFoundError("One or more input files do not exist")

    # If all OK or not in strict mode then proceed to copy existing files
    for infile, outfile, exists in zip(infiles, outfiles, infiles_exist):
        if exists:
            print(infile)
            shutil.copyfile(infile, outfile)

    if len(outfiles) > 0:
        subprocess.call(["tar", "-czf", args.output_tar_file, "-C", temp_dir.name, out_root])

    temp_dir.cleanup()


if __name__ == "__main__":
    main()
