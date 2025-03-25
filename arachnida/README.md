# Arachnida Project

This project contains two Python scripts, `scorpion.py` and `spider.py`, which respectively allow you to display the EXIF metadata of an image and download images recursively from a given URL. Both scripts can be executed within a Docker container.

## Features

### `scorpion.py`
- Displays the EXIF metadata of an image.
- Uses a graphical interface to show EXIF information and a preview of the image.
- Verifies that the file is a valid image before processing the data.

### `spider.py`
- Downloads images from a given URL.
- Works recursively to explore links and download all accessible images.
- Saves the images in a local directory.

## Prerequisites

- Docker
- Docker Compose

## Installation and Execution

1. Clone this repository to your local machine:
   ```sh
   git clone <REPOSITORY_URL>
   cd arachnida
   ```

2. Build and start the Docker container:
   ```sh
   docker compose up --build
   ```

3. Access the Docker container:
   ```sh
   docker exec -it python bash
   ```

4. Run the scripts as needed:

   - To display the EXIF metadata of an image using `scorpion.py`:
     ```sh
     python scorpion.py <PATH_TO_IMAGE>
     ```

   - To download images from a URL using `spider.py`:
     ```sh
     python spider.py <URL>
     ```

## Project Structure

```
arachnida/
├── docker-compose.yaml
├── dockerfile
├── README.md
└── file/
    ├── scorpion.py
    └── spider.py
```

- **`docker-compose.yaml`**: Docker Compose configuration file.
- **`dockerfile`**: Docker file to build the Python image.
- **`scorpion.py`**: Script to display the EXIF metadata of an image.
- **`spider.py`**: Script to recursively download images.

## Notes

- Ensure that the images to be analyzed with `scorpion.py` are accessible from the Docker container.
- Images downloaded by `spider.py` will be saved in the container's local directory.