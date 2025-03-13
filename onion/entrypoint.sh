#!/bin/sh

# Function to restart tor service
restart_tor() {
    echo "Stopping tor service..."
    service tor stop
    if [ $? -ne 0 ]; then
        echo "Failed to stop tor service. Checking if tor is running..."
        pgrep tor
        if [ $? -eq 0 ]; then
            echo "Tor is still running. Killing tor process..."
            pkill tor
        else
            echo "Tor is not running."
        fi
    fi

    echo "Starting tor service..."
    service tor start
    if [ $? -ne 0 ]; then
        echo "Failed to start tor service."
        exit 1
    fi
}

# Restart tor service
restart_tor

# Start SSH service
service ssh start

# Print the hostname of tor
cat /var/lib/tor/my_website/hostname 


# Start nginx
nginx -g "daemon off;"

# sudo docker run -d -p 8080:80 --name myapp_container myapp
# sudo docker exec -it myapp_container /bin/bash
# sudo docker run -p 80:80 -p 4242:4242 myapp