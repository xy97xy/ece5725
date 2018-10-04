
import RPi.GPIO as GPIO
import time
import sys 

#frequency = 50
dc = 7.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.OUT)
code_running = True
 
def GPIO17_callback(channel):
    global code_running
    code_running = False
p = GPIO.PWM(6, 10)
GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
#GPIO.wait_for_edge(17, GPIO.FALLING)
p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100.0)

#ip.ChangeFrequency(freq) # where freq is the new frequency in Hz

#p.ChangeDutyCycle(dc) # where 0.0 <= dc <= 100.0

#p.stop()

#p = GPIO.PWM(GPIO_pin, frequency)

while code_running:
    try:
        for h in range(150, 129, -2):
            #print dc/100.0
            frequency = 100000/(h + 2000.0)
            p.ChangeFrequency(frequency)
            dc = h/(h+2000.0)*100
            p.ChangeDutyCycle(dc)
            print(dc, frequency)
            time.sleep(3)
        for h in range(150, 171, 2): 
            frequency = 100000/(h + 2000.0)
            p.ChangeFrequency(frequency)
            dc = h/(h+2000.0) *100
            p.ChangeDutyCycle(dc)
            print(dc, frequency)
            time.sleep(3)
        code_running = False
    except KeyboardInterrupt:
        code_running = False

p.stop()
GPIO.cleanup()
