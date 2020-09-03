import board
import configparser
import time
import board
import busio
import adafruit_bme280

import click
from  paho.mqtt import publish


i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

config = configparser.ConfigParser()
config.read('config.ini')

sampling_rate = 1/float(config['temp_humidity']['samples_per_second'])
hostname = config['mqtt']['hostname']
publish.single("incubator/1/log", "start_temp_humidity started", hostname=hostname)


while True:
    time.sleep(sampling_rate)
    try:
        h, t = bme280.humidity, bme280.temperature
        publish.single("incubator/1/humidity", h, hostname=hostname)
        publish.single("incubator/1/temperature", t, hostname=hostname)
    except (RuntimeError, OverflowError, OSError) as e:
        publish.single("incubator/1/error_log", f"start_temp_humidity.py failed: {str(e)}", hostname=hostname)
        time.sleep(5)

        i2c = busio.I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
