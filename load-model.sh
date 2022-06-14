#!/bin/bash

# Load pretrained model and move to the default directory
wget http://dl.turkunlp.org/turku-ner-models/combined-ext-model-130220.tar.gz
tar -xzf combined-ext-model-130220.tar.gz
mv combined-ext-model/ ner-model/
rm combined-ext-model-130220.tar.gz
