#!/bin/bash

# Install gdown if not already installed
if ! command -v gdown &> /dev/null
then
    echo "gdown could not be found, installing now"
    pip install gdown
fi

# Download files
gdown --output models/ https://drive.google.com/uc?id=140nWkufV4fjzb18Bs910KQldIcUeVwMc
gdown --output models/ https://drive.google.com/uc?id=1XP-jlvvDaFwaRDNIuJGF1ZzieSoNHzp_
gdown --output models/ https://drive.google.com/uc?id=1lmefcl-dvP9gwqwFUulZwp3_WuA_dgac