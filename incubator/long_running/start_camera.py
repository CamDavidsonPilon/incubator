import configparser
from io import BytesIO
from time import sleep
from picamera import PiCamera

import click
from  paho.mqtt import publish
import board


config = configparser.ConfigParser()
config.read('config.ini')

sampling_rate = 1/float(config['camera']['samples_per_second'])
hostname = config['network']['leader_hostname']
camera = PiCamera()
publish.single("incubator/1/log", "start_camera started", hostname=hostname)


while True:
    sleep(sampling_rate - 0.5)
    try:
        stream = BytesIO()
        camera.capture(stream, 'jpeg')
        b = bytearray(stream.getvalue())
        publish.single("incubator/1/camera", b, hostname=hostname)
        publish.single("incubator/1/log", "photo taken", hostname=hostname)
    except Exception as e:
       pass
