#!/usr/bin/python
import time
import RPi.GPIO as GPIO
 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
MotorPin=12
GPIO.setup(MotorPin,GPIO.OUT)
PWM_FREQ = 50
delay_time = 1
pwm_motor = GPIO.PWM(MotorPin, PWM_FREQ)
pwm_motor.start(7.5)

def Change_Angle(angle):
    dutycycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return dutycycle

def test(): 
    while True:
        for a in range(100):
            pwm_motor.ChangeDutyCycle(4)
            time.sleep(0.01)
#           pwm_motor.stop()
        for b in range(100):
            pwm_motor.ChangeDutyCycle(7.5)
            time.sleep(0.01)
#       pwm_motor.stop()
        for c in range(100):
            pwm_motor.ChangeDutyCycle(11)
            time.sleep(0.01)
#       pwm_motor.stop()
        for d in range(100):
            pwm_motor.ChangeDutyCycle(7.5)
            time.sleep(0.01)

if __name__ == '__main__' :
    pwm_motor.ChangeDutyCycle(Change_Angle(15))
    time.sleep(delay_time)
    print("Angle: 15")
    time.sleep(5)
    """
    pwm_motor.ChangeDutyCycle(Change_Angle(165))
    time.sleep(delay_time)
    print("Angle: 165")
    time.sleep(1)
    """
    pwm_motor.ChangeDutyCycle(Change_Angle(45))
    time.sleep(delay_time)
    print("Angle: 45")
    time.sleep(5)
    """
    pwm_motor.ChangeDutyCycle(Change_Angle(135))
    time.sleep(delay_time)
    print("Angle: 135")
    time.sleep(1)
    """
    pwm_motor.ChangeDutyCycle(Change_Angle(75))
    time.sleep(delay_time)
    print("Angle: 75")
    time.sleep(5)
    """
    pwm_motor.ChangeDutyCycle(Change_Angle(105))
    time.sleep(delay_time)
    print("Angle: 105")
    """
    pwm_motor.ChangeDutyCycle(Change_Angle(90))
    time.sleep(delay_time)
    print("Angle: 90")