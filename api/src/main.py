from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
from air_sensor import AirSensor
from light_sensor import LightSensor
import json
import os
import mimetypes
from datetime import datetime

import paho.mqtt.client as mqtt

air_sensor = AirSensor()
light_sensor = LightSensor()

host = "0.0.0.0"
port = 5000

# Get environment stuff
mqtt_host = os.getenv("MQTT_HOST", "10.5.61.199")
mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
server_id = os.getenv("SERVER_ID", "7")

def on_connect(client, userdata, flags, reason_code, properites):
    print(f"Connected to MQTT Broker with result {reason_code}")

def on_message(client, userdata, message):
    return

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_host, mqtt_port, 60)

sleep(1)


class Server(BaseHTTPRequestHandler):
    def sendJSON(self, object: object, code: int = 200):
        self.send_response(code)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Vary", "Origin")
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(object).encode())

    def serveStatic(self):
        local_file_path = os.path.join(".", self.path[1:], "index.html")
        print(local_file_path)

        if os.path.exists(local_file_path) and os.path.isfile(local_file_path):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "*")
            self.send_header("Access-Control-Allow-Headers", "*")
            self.send_header("Vary", "Origin")

            mime_type, _ = mimetypes.guess_type(local_file_path)
            if mime_type:
                self.send_header("Content-type", mime_type)
            else:
                self.send_header("Content-type", "application/octet-stream")

            self.end_headers()

            with open(local_file_path, "rb") as file:
                self.wfile.write(file.read())

    def do_GET(self):
        # Send MQTT
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        mqtt_client.publish(f"raspi/{server_id}/http/request", f"Last request: {now}", qos=2)

        if self.path == "/api/sensors":
            air = air_sensor.readAir()
            light = light_sensor.readLight()
            self.sendJSON({
                "status": "ok",
                "data": [
                    {"label": "Temperature", "value": air.temperature, "unit": "°C"},
                    {"label": "Humidity", "value": air.humidity, "unit": "%"},
                    {"label": "Light", "value": light, "unit": "lux"}
                ]
            })

def main():
    web_server = HTTPServer((host, port), Server)
    print(f"Server started and listen to {host}:{port}")

    try:
        mqtt_client.loop_start()
        mqtt_client.publish("leonardoevic/up", "true", qos=2)
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

print("Server stopped")
 
