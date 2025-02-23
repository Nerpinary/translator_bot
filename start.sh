#!/bin/bash

mkdir -p models

if [ ! -d "models/vosk-model-ru" ]; then
    echo "Downloading Vosk model..."
    cd models
    curl -O https://alphacephei.com/vosk/models/vosk-model-ru-0.22.zip
    unzip vosk-model-ru-0.22.zip
    mv vosk-model-ru-0.22 vosk-model-ru
    rm vosk-model-ru-0.22.zip
    cd ..
fi

python3 run.py