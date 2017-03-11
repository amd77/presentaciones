#!/usr/bin/python

from __future__ import absolute_import

# el OE de l pwm.* es el gpio 13
# boton el 18 y el 22 pullup
# servo1 el pwm.9, servo2 el pwm.10
# motor el 19 standby a 1, motor1 pwm.14 27-23 giro, motor2 13 pwm 6-5 giro
# led pin 24
# led1 pwm.0 pwm.1 pwm.2
# led2 pwm.3 pwm.4 pwm.15

# acelerometro MMA8453Q i2C slave addr 001110X 0011100
# sensor de luz analog.5
# sensor de temperatura analog.4

import RPi.GPIO as GPIO
from Adafruit_PWM_Servo_Driver import PWM
from Adafruit_I2C import Adafruit_I2C
import time
import os
import json


if True:  # setup globales

    # pines en modo broadcom
    GPIO.setmode(GPIO.BCM)

    # standby a 1
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, 1)

    # Initialise the PWM
    pwm = PWM(0x7F)

    # Set frequency to 50 Hz
    pwm.setPWMFreq(50)

    # Initialise the ADC
    adc = Adafruit_I2C(0x48)


def lee_sensor(channel=5):
    if channel % 2 == 0:
        c = channel // 2
    else:
        c = (channel - 1) // 2 + 4
    reg = 0x84 | (c << 4)
    # Read the light sensor
    adc.writeRaw8(reg)
    return adc.readU8(reg)


class Persistencia(object):
    path = "/var/run/robocop/"

    def __init__(self, filename):
        self.fullpath = self.path + filename
        if not os.path.isdir(self.path):
            raise RuntimeError("Carpeta {} no existente".format(self.path))
        if not os.path.isfile(self.fullpath):
            self.guarda(0)

    def guarda(self, valor):
        actual = json.load(open(self.fullpath))
	if actual != valor:
            json.dump(valor, open(self.fullpath, "w"))

    def valor(self):
        if os.path.isfile(self.fullpath):
            return json.load(open(self.fullpath))
        else:
            raise RuntimeError("Fichero {} no existente".format(self.fullpath))


class Servo(Persistencia):
    def __init__(self, filename, pwm_id):
        super(Servo, self).__init__(filename)
        self.pwm_id = pwm_id
        self.velocidad(0)

    def velocidad(self, valor=None):  # valor entre 0 y 1
        if valor is None:
            valor = self.valor()
        if valor == 0:
            pwm.setPWM(self.pwm_id, 4096, 0)
        elif abs(valor) <= 1:
            pwm.setPWM(self.pwm_id, 0, int(4096 * abs(valor)))
        else:
            raise RuntimeError("Valor incorrecto: {}".format(valor))


class Motor(Servo):
    def __init__(self, filename, pwm_id, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.output(self.pin1, 0)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.output(self.pin2, 0)
        super(Motor, self).__init__(filename, pwm_id)

    def velocidad(self, valor=None):
        super(Motor, self).velocidad(valor)
        if valor is None:
            valor = self.valor()

        if valor == 0:
            GPIO.output(self.pin1, 0)
            GPIO.output(self.pin2, 0)

        elif valor > 0:
            GPIO.output(self.pin1, 1)
            GPIO.output(self.pin2, 0)

        else:  # valor < 0:
            GPIO.output(self.pin1, 0)
            GPIO.output(self.pin2, 1)


class Boton(Persistencia):
    def __init__(self, filename, pin):
        super(Boton, self).__init__(filename)
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)

    def pulsado(self):
        value = not GPIO.input(self.pin)
        self.guarda(value)
        return value


if __name__ == "__main__":
    # definicion de pines
    rueda_drcha = Motor("rueda_drcha", 14, 27, 23)
    rueda_izqda = Motor("rueda_izqda", 13, 6, 5)
    brazo_drcha = Servo("brazo_drcha", 9)
    brazo_izqda = Servo("brazo_izqda", 10)
    boton1 = Boton("boton1", 18)
    boton2 = Boton("boton2", 22)

    try:
        while True:
            if boton1.pulsado():
                pass  # break
            if boton2.pulsado():
                pass  # break
            brazo_drcha.velocidad()
            brazo_izqda.velocidad()
            rueda_drcha.velocidad()
            brazo_izqda.velocidad()
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    for cosa in [brazo_drcha, brazo_izqda, rueda_drcha, rueda_izqda]:
        cosa.velocidad(0)
    GPIO.cleanup()
