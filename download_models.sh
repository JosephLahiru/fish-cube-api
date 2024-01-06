#!/bin/bash

if ! command -v gdown &> /dev/null
then
    echo "gdown could not be found, installing now"
    pip install gdown
fi

gdown --output modelss/ https://drive.google.com/uc?id=140nWkufV4fjzb18Bs910KQldIcUeVwMc
gdown --output modelss/ https://drive.google.com/uc?id=1XP-jlvvDaFwaRDNIuJGF1ZzieSoNHzp_
gdown --output modelss/ https://drive.google.com/uc?id=1hTbFKPYOlSa13ew-hvxjVoXLbLqsbuYD