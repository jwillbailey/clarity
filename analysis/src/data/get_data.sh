#!/bin/bash

# Get the raw data

ROOT=$(pwd)/../..

# Update the external transcription files
(
    cd $ROOT/data/external
    git -C clarity_transcriber pull || git clone git@github.com:claritychallenge/clarity_transcriber.git
)

# Make the symbolic link to the downloaded data if it doesn't exist
if [ ! -L $ROOT/data/raw/transcriptions ]; then
    (
        cd $ROOT/data/raw
        ln -s ../external/clarity_transcriber/data/transcriptions .
    )
fi

# Fetch BEEP pronunciation dictionary
if [ ! -d $ROOT/data/beep ]; then
    wget https://www.openslr.org/resources/14/beep.tar.gz
    tar -xzf beep.tar.gz
    mv beep $ROOT/data/external
    rm beep.tar.gz
fi
