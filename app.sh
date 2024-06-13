#!/bin/bash

# Argument provided to the script (path to the image or video)
FILE="$1"

# Change directory to the yolo folder
cd yolo

# Remove the directory ./runs/detect
rm -rf ./runs/detect

# Run the Python script traffic-monitor.py with the provided source file as an argument
# Specify the weights file to use and enable saving cropped images
python traffic-monitor.py --source "$FILE" --weights 'runs/train/exp/weights/best.pt' --save-crop

# Change directory back to the parent directory
cd ..

# Run the Python script main.py
python main.py
