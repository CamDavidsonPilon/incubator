import board
from adafruit_dht import DHT22
import configparser
import time
import RPi.GPIO as GPIO

import click
from  paho.mqtt import publish


config = configparser.ConfigParser()
config.read('config.ini')

dht22 = DHT22(board.D21)
sampling_rate = 1/float(config['temp_humidity']['samples_per_second'])
hostname = config['mqtt']['hostname']
publish.single("incubator/1/log", "start_temp_humidity started", hostname=hostname)


while True:
    time.sleep(sampling_rate)
    try:
        h, t = dht22.humidity, dht22.temperature
        publish.single("incubator/1/humidity", h, hostname=hostname)
        publish.single("incubator/1/temperature", t, hostname=hostname)
    except (RuntimeError, OverflowError) as error:
        print(error.args[0])
        # restart
        GPIO.cleanup()
        dht22 = DHT22(board.D21)
