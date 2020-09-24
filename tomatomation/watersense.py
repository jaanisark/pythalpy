# External Module Imports
import RPi.GPIO as GPIO
import time
import sys

# Pin Definitions:
h2oPin = 14 #BCM Pin 14, Board Pin 8
pumpPin = 21 #BCM Pin 21, Board Pin 40
ledPin = 15 #BCM

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(h2oPin, GPIO.IN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(pumpPin, GPIO.OUT, initial=GPIO.LOW)

# PWM Initialization (Pin, Frequency):
pumpPWM = GPIO.PWM(pumpPin, 25)
ledPWM = GPIO.PWM(ledPin, 100)
ledPWM.start(0)
pumpPWM.start(0)

# Sensing
water_sense = 0 # Initial Water Sensor Value: False
w_time_hr = 8 # Set Scheduler to Start at 8 AM
watering_complete = False #initial value, may not be req'd

# Pump Actions
def start_pump():
    pumpPWM.ChangeDutyCycle(100)
    ledPWM.ChangeDutyCycle(100)
    print("Starting Water Pump at "+str(time.ctime())+"!")  

def stop_pump():
    pumpPWM.ChangeDutyCycle(0) # Shutoff Pump
    ledPWM.ChangeDutyCycle(0) # Turn On Status LED   
    end_time = time.time() # Capture End Time
    total_duration = end_time - start_time
    print("Total Pumping Time = " + str(round(total_duration)) + " seconds")

try:
    while running:
        c_time=time.localtime() #Get Current Time
        w_time_hr = c_time.tm_hour # FORCE START FOR TESTING
        if c_time.tm_hour == w_time_hr:
            print("Watering Started On "+str(time.ctime())"!")
            start_time = time.time()  
            start_pump()
            while watering_complete == False:
                water_sense = GPIO.input(h2oPin) # Check Water Sensor Status
                if (time.time() - start_time) > 3 and water_sense == 1: # Minimum Pump Runtime: 3 seconds and Sensor Check
                    stop_pump()
                    watering_complete = True
                    print("Water Detected! Pump Off")
                elif (time.time() - start_time) > 60:
                    stop_pump()
                    watering_complete = True
                    print("Pump Time Maxed Out, Shutting Off Pump!")              
                else:
                    print("No Water Detected. Continue Pumping")
                    time.sleep(1)
            time.sleep(3600)
        else:
            time.sleep(60)
            print("It's not time to water yet. Watering scheduled for hour #" + w_time_hr + " of 24")

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    print("Program Interrupted By Keyboard")
    stop_pump()
    GPIO.cleanup()
    sys.exit()


#w_time_hr = c_time.tm_hour # FOR TESTING: ***Force Start NOW***
