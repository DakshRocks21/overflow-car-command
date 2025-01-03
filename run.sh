#!/bin/bash

set -e

usage() {
    echo "Usage: $0 [--full]"
    echo "  --full    Install all dependencies before running the project."
    exit 1
}

# Check for --full flag
INSTALL_FULL=false
if [[ "$1" == "--full" ]]; then
    INSTALL_FULL=true
elif [[ -n "$1" ]]; then
    usage
fi

echo "Starting Overflow Open House RC Car Project 🚗💨"

if [ -f config.env ]; then
    echo "Loading environment variables from config.env file..."
    export $(grep -v '^#' config.env | xargs)
else
    echo "Error: config.env file not found. Please create it using the config.sample.env template."
    exit 1
fi

if [ "$INSTALL_FULL" = true ]; then
    echo "Installing all system dependencies..."
    sudo apt update
    sudo apt install -y python3-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0 libcairo2-dev \
    libgirepository1.0-dev libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools \
    gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio libglib2.0-dev libgstrtspserver-1.0-dev gstreamer1.0-rtsp
    echo "System dependencies installed!"
else
    echo "Skipping full dependency installation. Run with --full to install dependencies."
fi

echo "Starting motor control script..."
python3 car.py &

CAR_PID=$!

echo "Starting WebSocket and RTSP server..."
python3 main.py &

MAIN_PID=$!

trap "echo 'Shutting down...'; kill $CAR_PID $MAIN_PID; exit" SIGINT SIGTERM

wait $CAR_PID $MAIN_PID
