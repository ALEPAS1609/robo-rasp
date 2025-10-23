import RPi.GPIO as GPIO
from config import *

class DriveBase:
    def __init__(self):
        # Motor LX pins
        self.IN1 = motor_pin1  # PWM pin for motor LX
        self.IN2 = motor_pin2  # PWM pin for motor LX

        # Motor RX pins
        self.IN3 = motor_pin3  # PWM pin for motor RX
        self.IN4 = motor_pin4  # PWM pin for motor RX

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)

        # Initialize PWM for motor LX and RX
        self.pwm_lx0 = GPIO.PWM(self.IN1, 1000)  # 1000 Hz frequency
        self.pwm_lx1 = GPIO.PWM(self.IN2, 1000)
        self.pwm_rx0 = GPIO.PWM(self.IN3, 1000)
        self.pwm_rx1 = GPIO.PWM(self.IN4, 1000)
        self.pwm_lx0.start(0)    # Start with 0% duty cycle (stopped)
        self.pwm_lx1.start(0)  
        self.pwm_rx0.start(0)
        self.pwm_rx1.start(0)

    def rx(self, speed):
        if speed >=0:
            self.pwm_rx0.ChangeDutyCycle(speed)
            self.pwm_rx1.ChangeDutyCycle(0)
        else:
            self.pwm_rx1.ChangeDutyCycle(abs(speed))
            self.pwm_rx0.ChangeDutyCycle(0)

    def lx(self, speed):
        if speed >=0:
            self.pwm_lx0.ChangeDutyCycle(speed)
            self.pwm_lx1.ChangeDutyCycle(0)
        else:
            self.pwm_lx1.ChangeDutyCycle(abs(speed))
            self.pwm_lx0.ChangeDutyCycle(0)

    def run(self, speed, angle):
        speedr = speed * ((90-abs(angle))/90)
        if(angle >=0):
            self.lx(speed)
            self.rx(speedr)
        else:
            self.lx(speedr)
            self.rx(speed)

    def stop(self):
        """Stop both motors."""
        self.pwm_lx0.ChangeDutyCycle(0)
        self.pwm_lx1.ChangeDutyCycle(0)
        self.pwm_rx0.ChangeDutyCycle(0)
        self.pwm_rx1.ChangeDutyCycle(0)

    def cleanup(self):
        """Clean up GPIO."""
        self.pwm_lx0.stop()
        self.pwm_lx1.stop()
        self.pwm_rx0.stop()
        self.pwm_rx1.stop()
        GPIO.cleanup()

