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
hostname = config['mqtt']['hostname']
camera = PiCamera()


while True:
    sleep(sampling_rate - 0.5)
    try:
        stream = BytesIO()
        sleep(0.5)
        camera.capture(stream, 'jpeg')
        b = bytearray(stream.getvalue())
        publish.single("incubator/camera", b, hostname=hostname)
    except RuntimeError as error:
       print(error.args[0])
