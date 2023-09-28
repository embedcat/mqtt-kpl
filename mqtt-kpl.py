import json
import logging
import os
import random
import paho.mqtt.client as mqtt_client
from datetime import datetime

MQTT_BROKER_IP = "176.57.218.132"
MQTT_BROKER_PORT = 1883
EVENTS_PATH = "events"
LOGGING_FILE = "log_mqtt_client.log"


logger = logging.getLogger("mqtt-kpl")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOGGING_FILE, mode='w')
ch = logging.StreamHandler()
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


client = mqtt_client.Client()


def write_logline(filename: str, text: str) -> None:
    with open(filename, "a") as logfile:
        now = datetime.strftime(datetime.now(), "%d-%m-%Y %H:%M:%S")
        log_text = f"[{now}] {text}\n"
        writed = logfile.write(log_text)


def _store_message(message: mqtt_client.MQTTMessage):
    modem_id = str(message.topic.split("/")[0] if "/" in message.topic else message.topic)
    write_logline(f"{EVENTS_PATH}/{modem_id}.log", f"{str(message.topic)}: {message.payload.decode('utf-8')}")


def _on_connect(client, userdata, flags, rc):
    logger.info("Connected")
    client.subscribe(f"#")


def _on_disconnect(client, userdata, rc):
    logger.info("Disconnected")


def _on_message(client, userdata, message):
    logger.info(f"Msg received. Topic: <{message.topic}>. Msg: <{message.payload}>")
    _store_message(message=message)


def _on_publish(client, userdata, message):
    logger.info(f"Msg published. Topic: <{message.topic}>. Msg: <{message.payload.decode('utf-8')}>")


def _on_subscribe(client, userdata, mid, granted_qos):
    logger.info(f"Subscribed")


def main():
    logger.info("MQTT Client script started")

    if not os.path.exists(EVENTS_PATH):
        os.makedirs(EVENTS_PATH)

    # client.username_pw_set(settings.MQTT_BROKER_USERNAME, settings.MQTT_BROKER_PASSWORD)
    client.on_connect = _on_connect
    client.on_message = _on_message
    client.on_publish = _on_publish
    client.on_disconnect = _on_disconnect
    client.on_subscribe = _on_subscribe

    client.connect(host=MQTT_BROKER_IP, port=int(MQTT_BROKER_PORT))
    client.loop_forever()
    # client.connect_async(host=MQTT_BROKER_IP, port=int(MQTT_BROKER_PORT))
    # client.loop_start()


if __name__ == "__main__":
    main()
