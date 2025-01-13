#!/bin/bash

# Set up logging
LOG_DIR="./logs"
mkdir -p $LOG_DIR
MEDIAMTX_LOG="$LOG_DIR/mediamtx.log"
CAR_LOG="$LOG_DIR/car.log"
MAIN_LOG="$LOG_DIR/main.log"

echo "Starting mediamtx..."
./mediamtx > $MEDIAMTX_LOG 2>&1 &
MEDIAMTX_PID=$!
echo "mediamtx started with PID $MEDIAMTX_PID"

echo "Starting car.py..."
python3 car.py > $CAR_LOG 2>&1 &
CAR_PID=$!
echo "car.py started with PID $CAR_PID"

sleep 5
echo "Starting main.py..."
python3 main.py > $MAIN_LOG 2>&1 &
MAIN_PID=$!
echo "main.py started with PID $MAIN_PID"

echo "All processes started."

# Wait for all processes
wait $CAR_PID 

echo "All processes have stopped."

