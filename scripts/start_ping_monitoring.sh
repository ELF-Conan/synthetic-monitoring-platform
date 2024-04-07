#!/bin/bash

LOG_DIR="/var/monitoring"
LOG_FILE="$LOG_DIR/ping_monitoring.log"

if [ ! -d "$LOG_DIR" ]; then
    echo "Log directory $LOG_DIR does not exist. Creating..."
    mkdir -p "$LOG_DIR"
    if [ $? -ne 0 ]; then
        echo "Failed to create log directory. Exiting."
        exit 1
    fi
    echo "Log directory created."
fi

echo "Starting the monitoring platform in the background..."

nohup python3 ../synthetic_monitoring/main.py > $LOG_FILE 2>&1 &

echo "Monitoring platform started."