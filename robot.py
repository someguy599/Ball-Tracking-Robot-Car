import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
import cv2
import numpy as np
from gpiozero import DistanceSensor
from gpiozero import InputDevice

rightreverse = 20
rightforward = 21
leftreverse = 19
leftforward = 26
movementpins = [rightreverse, rightforward, leftreverse, leftforward]

sensorone = InputDevice(27)
sensortwo = InputDevice(24)

GPIO.setmode(GPIO.BCM)
camera = Picamera2()
camera_config =  camera.create_preview_configuration(main={"format": "RGB888", "size": (320, 240)})
camera.configure(camera_config)

camera.start()
time.sleep(1)

for gpin in movementpins:
    GPIO.setup(gpin, GPIO.OUT)
    GPIO.output(gpin, GPIO.LOW)

def obstacle_check():
    if sensorone.is_active and sensortwo.is_active:
        print("No obstacles detected!")
        return False
    else:
        print("Obstacle detected!")
        return True

def move_reverse():
    GPIO.output(leftforward, GPIO.LOW)
    GPIO.output(rightforward, GPIO.LOW)
    GPIO.output(leftreverse, GPIO.HIGH)
    GPIO.output(rightreverse, GPIO.HIGH)

def move_forward():
    GPIO.output(leftforward, GPIO.HIGH)
    GPIO.output(rightforward, GPIO.HIGH)
    GPIO.output(leftreverse, GPIO.LOW)
    GPIO.output(rightreverse, GPIO.LOW)

def move_right():
    GPIO.output(leftforward, GPIO.HIGH)
    GPIO.output(rightforward, GPIO.LOW)
    GPIO.output(leftreverse, GPIO.LOW)
    GPIO.output(rightreverse, GPIO.LOW)

def move_left():
    GPIO.output(leftforward, GPIO.LOW)
    GPIO.output(rightforward, GPIO.HIGH)
    GPIO.output(leftreverse, GPIO.LOW)
    GPIO.output(rightreverse, GPIO.LOW)

def stop():
    GPIO.output(leftforward, GPIO.LOW)
    GPIO.output(rightforward, GPIO.LOW)
    GPIO.output(leftreverse, GPIO.LOW)
    GPIO.output(rightreverse, GPIO.LOW)

def sensor_hit_obstacle():
    GPIO.input(sensor)

lower_color_range = np.array([121,140,1])
upper_color_range = np.array([180, 255, 255])
    
try: 
    while True:
        image = camera.capture_array()
        
        image_frame = cv2.GaussianBlur(image, (11, 11), 0)
        hsv_conversion = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)
        
        color_mask = cv2.inRange(hsv_conversion, lower_color_range, upper_color_range)
        color_mask = cv2.erode(color_mask, None, iterations=2)
        color_mask = cv2.dilate(color_mask, None, iterations=2)
        
        contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        object_area = 0
        object_x = 0
        object_y = 0

        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            print(f"({x},{y}),{width},{height}")
            found_area = width * height
            center_x = x + (width/2)
            center_y = y + (height/2)
            if object_area < found_area:
                object_area = found_area
                object_x = center_x
                object_y = center_y

        print(f"Final( 0-140  140-180  180-320): ({object_x},{object_y}), Area: {object_area}")

        if object_area <= 0:
            print("No Object Found")
            move_left()
            time.sleep(0.001)

        if 0 <= object_x < 140:
            print("Moving Left")
            move_left()
            time.sleep(0.015)
            stop()
        elif object_x < 180:
            if obstacle_check():
                stop()
                time.sleep(0.04)
            else:
                print("Moving forward")
                move_forward()
                time.sleep(0.04)
        elif object_x <= 320:
            print("Moving right")
            move_right()
            time.sleep(0.015)

        stop()
        
except KeyboardInterrupt:
    print("\nProgram Terminated")

finally:
    GPIO.cleanup()
    cv2.destroyAllWindows()
    camera.stop()