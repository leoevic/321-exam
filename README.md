# Modul 321: Practical exam project

## Prerequisites

- Joy-Pi with installed operating system
- Docker is installed on the Joy-Pi

## Running the project

To run the project, just type in the following command:

```bash
sudo docker compose up --build
```

This will build the Docker image and run the project.

**Note:** This project uses the alternative lgpio library. The `lg.zip` file contains this library. It is unzipped and installed automatically during the build process of the image.

**Note:** The application code itself isn't copied into the image itself when building the Docker image, but mounted when launching the service using the Docker Compose file.

## Usage

To get data from the API, send a `GET` request to the following URL:

```
http://[host]:5000/api/sensors
```

With every request, the server will send a MQTT message to the central broker which contains the timestamp when the last request happened. The following topic is used to send the message:

```
/raspi/7/http/request
```

Sample message:

```
Last request: 2026-09-28T08:47:49
```