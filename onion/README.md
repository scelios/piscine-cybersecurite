# Onion Project

This project sets up a Docker container with Tor, Nginx, Apache2, and SSH services. It also includes a simple web page served by Nginx and a service configuration for Tor.

## Prerequisites

- Docker
- Docker Compose (optional)

## Getting Started

### Build the Docker Image

To build the Docker image, navigate to the project directory and run:

```sh
sudo docker build -t onion_project .
```

### Run the Docker Container

To run the Docker container, use the following command:

```sh
sudo docker run -p 8080:80 -p 4242:4242 --name onion_container onion_project
```

### Accessing the Services

- **Nginx Web Server**: Open your browser and navigate to `http://localhost:8080` to see the web page served by Nginx.
- **SSH**: Connect to the container via SSH using the following command:
  ```sh
  ssh -p 4242 appuser@localhost
  ```
  Use the password `password` for the `appuser`.

### Tor Hidden Service

The Tor hidden service is configured to serve the Nginx web page. To access the hidden service, you need to have Tor installed on your local machine. Use the following command to start Tor:

```sh
tor
```

Then, navigate to the hidden service URL specified in the `/var/lib/tor/my_website/hostname` file inside the container.

### Viewing Logs

To view the SSH logs, you can access the container and check the `/var/log/auth.log` file:

```sh
sudo docker exec -it onion_container /bin/bash
cat /var/log/auth.log
```

## Configuration Files

- **nginx.conf**: Configuration file for Nginx located at `/etc/nginx/nginx.conf`.
- **sshd_config**: Configuration file for SSH located at `/etc/ssh/sshd_config`.
- **torrc**: Configuration file for Tor located at `/etc/tor/torrc`.

## Project Structure

```
/home/hall/piscine/onion/
├── .vscode/
│   ├── c_cpp_properties.json
│   ├── launch.json
│   └── settings.json
├── src/
│   └── index.html
├── entrypoint.sh
├── nginx.conf
├── requirements.txt
├── sshd_config
├── torrc
└── dockerfile
```

## Notes

- The SSH configuration is set to allow only key-based authentication for the `appuser`.
- The root login is disabled via password for security reasons.
- The project includes a fake SSH key for demonstration purposes. Replace it with your actual SSH key for real use.

## License

This project is for educational purposes and does not include a specific license.