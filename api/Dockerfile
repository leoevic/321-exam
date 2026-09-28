FROM python:3.12

RUN apt-get update

RUN apt install -y swig python3-dev

RUN pip install setuptools

COPY ./lg.zip .

RUN unzip lg.zip

WORKDIR /lg

RUN make

RUN make install

RUN pip install smbus paho-mqtt rpi-lgpio

RUN pip install dht11 --no-deps

ENV MQTT_HOST="10.5.61.199"

ENV MQTT_PORT="1883"

ENV SERVER_ID="7"

WORKDIR /usr/src/app