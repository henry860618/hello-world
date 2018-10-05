import CarControl
import sys
import time
import RPi.GPIO as GPIO
import termios
import tty
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 
GPIO_TRIGGER = 16 
GPIO_ECHO = 18
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# ---------------- UltraSonic ----------------
MotorPin = 12
GPIO.setup(MotorPin, GPIO.OUT)
PWM_FREQ = 50
pwm_motor = GPIO.PWM(MotorPin, PWM_FREQ) # 1 wave time = 1 / 50 = 0.02 s = 20 ms
pwm_motor.start(7.25)
delay_time = 1
# --- Map ---
target_angle = 0
target_distance = 0
axis_X = 0
axis_Y = 0


def Set_Moter_Angle(value):
    if value >= 3 and value <= 12 :
        pwm_motor.ChangeDutyCycle(value)
        time.sleep(delay_time)
    else :
        print ("Moter Error.")

def Send_Trigger():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.01)
    GPIO.output(GPIO_TRIGGER, False)

def Wait_Echo(value, timeout):
    count = timeout
    while GPIO.input(GPIO_ECHO) != value and count > 0 :
        count = count - 1

def GetDistance():
    Send_Trigger()
    Wait_Echo(True, 5000)
    start = time.time()
    Wait_Echo(False, 5000)
    finish = time.time()
    PulseLen = finish - start
    distance = PulseLen * 340 * 100 / 2     # cm
    return (distance)
# ---------------- UltraSonic ----------------
def Change_Angle(angle):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def CheckAllAngle() :
    angle_list = []
    now_angle = 30
    for i in range(5) :
        Set_Moter_Angle(Change_Angle(now_angle))
        distance = GetDistance()
        angle_list.append(distance)
        now_angle = now_angle + 30
    return angle_list

def Turn_Angle(angle) :

    if angle < 90 :
        angle = 90 - angle
        if angle > 100 :
            CarControl.TurnR_Fast(0.1, 30, 30)
        elif angle > 50 and angle < 100 :
            CarControl.TurnR_Fast(0.1, 30, 20)
        else :
            CarControl.TurnR_Fast(0.1, 40, 15)
    elif angle > 90 :
        angle = angle - 90
        if angle > 100 :
            CarControl.TurnL_Fast(0.1, 30, 30)
        elif angle > 50 and angle < 100 :
            CarControl.TurnL_Fast(0.1, 30, 20)
        else :
            CarControl.TurnL_Fast(0.1, 40, 15)
    time.sleep(delay_time)

def Back_to_positive(target_angle, move) :    ###
    CarControl.Pause(0.1)
    move_distance = 0 
    if target_angle != 0 :
        turn_angle = 90 + target_angle 
        Turn_Angle(turn_angle)

        if abs(target_angle) == 30 :
            move_distance = int(move * math.sqrt(3) / 2)
        elif abs(target_angle) == 60 :
            move_distance = int(move / 2)
    else :
        move_distance = move

    return move_distance

def Check_Can_Forward(direction_list):
    if (direction_list[0] < 15 and direction_list[4] < 15) or (direction_list[1] < 30 and direction_list[3] < 30) :
        print("Middle can't pass") # if can't pass
        CarControl.Backward(0.1, 25, 15)
        Turn_Angle(60)
        return_angle = 30
    elif direction_list[0] < 15 or direction_list[1] < 30 :
        print("Right can't pass") # if can't pass
        Turn_Angle(120)
        return_angle = -30
    elif direction_list[4] < 15 or direction_list[3] < 30 :
        print("Left can't pass") # if can't pass
        Turn_Angle(60)
        return_angle = 30
    else :
        return 0
    
    return return_angle

def New_UltraSonic(target_angle, target_distance) : ###
    
    while target_distance > 0 :
        print('---------------------------------')
        print('Now target_angle:', target_angle)
        print('Now target_distance:', target_distance)
        CarControl.Pause(0.1)
        direction_list = CheckAllAngle()
        print(direction_list)
        Set_Moter_Angle(Change_Angle(90))
        if direction_list[2] > 60 : # forward can go
            Check_Forward = Check_Can_Forward(direction_list)
            print('You should turn', Check_Forward,'degrees')
            if Check_Forward == 0 :
                temp_distance = target_distance - int(direction_list[2]/2)
                if temp_distance > 0 :
                    print("Forward distance:", int(direction_list[2]/2))
                    CarControl.Forward(0.1, 25, int(direction_list[2]/4))
                    target_distance = target_distance - Back_to_positive(target_angle, int(direction_list[2]/2))
                else :
                    print("Forward distance:", target_distance)
                    CarControl.Forward(0.1, 25, target_distance) # go to target
                    target_distance = target_distance - Back_to_positive(target_angle, target_distance)
                target_angle = 0
            else :
                target_angle = target_angle + Check_Forward
        elif direction_list[1] > 60 or direction_list[3] > 60 :
            if direction_list[1] > direction_list[3] :
                turn_angle = 30
            else : 
                turn_angle = 120
            print("Turn Angle:", turn_angle)
            Turn_Angle(turn_angle)
            target_angle = target_angle + (90 - turn_angle)
        elif max(direction_list) > 60 : # find the best way
            direction = direction_list.index(max(direction_list))
            turn_angle = 30 + 30 * direction
            if turn_angle != 90 : # turn to correct angle
                print("Turn Angle:", turn_angle)
                Turn_Angle(turn_angle)
                target_angle = target_angle + (90 - turn_angle)
            else :
                Check_Forward = Check_Can_Forward(direction_list)
                print('You should turn', Check_Forward,'degrees')
                if Check_Forward == 0 :
                    temp_distance = target_distance - int(max(direction_list)/2)
                    if temp_distance > 0 :
                        print("Forward distance:", int(max(direction_list)/2))
                        CarControl.Forward(0.1, 25, int(max(direction_list)/4))
                        target_distance = target_distance - Back_to_positive(target_angle, int(max(direction_list)/2))
                    else :
                        print("Forward distance:", target_distance)
                        CarControl.Forward(0.1, 25, int(target_distance/2))
                        target_distance = target_distance - Back_to_positive(target_angle, target_distance)

                    target_angle = 0
                else :
                    target_angle = target_angle + Check_Forward
                   
        else : # max distance <= 60  //  all way can't go 
            CarControl.Backward(0.1, 25, 10)
            Turn_Angle(60)

if __name__ == '__main__' :
    try:
        global target_angle
        global target_distance
        target_angle = input('Target angle: ')
        target_angle = int(target_angle) 
        target_distance = input('Target distance(cm): ')
        target_distance = int(target_distance)
        
        Turn_Angle(target_angle)
        New_UltraSonic(0, target_distance)     
         
    except ValueError:
        CarControl.StopControl()
        ertype, message, traceback = sys.exc_info()
        while traceback:
            print('----Error Information-----')
            print(ertype)
            print(message)
            print(('function or module?', traceback.tb_frame.f_code.co_name))
            print(('file?', traceback.tb_frame.f_code.co_filename))
            traceback = traceback.tb_next
    except Exception:
        print('End of Program')
        CarControl.StopControl()
        GPIO.cleanup()
        ertype, message, traceback = sys.exc_info()
        while traceback:
            print('----Error Information-----')
            print(ertype)
            print(message)
            print(('function or module?', traceback.tb_frame.f_code.co_name))
            print(('file?', traceback.tb_frame.f_code.co_filename))
            traceback = traceback.tb_next





