#!/bin/bash

# Function to be executed when SIGTERM is received
on_sigterm() {
    echo "SIGTERM received, running the custom command..."
    # Place your custom command here
    # Example: echo "Performing pre-shutdown tasks"
    chmod -R 777 /var/lib/grafana/

    # Forward SIGTERM to the original entrypoint (Grafana)
    kill -TERM "$child" 2>/dev/null
}

# Trap SIGTERM
trap 'on_sigterm' SIGTERM

# Run the original Grafana entrypoint in the background
/run.sh &
child=$!
wait "$child"