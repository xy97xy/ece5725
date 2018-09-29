import time
import RPi.GPIO as GPIO
import os
import pygame
import subprocess

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 

os.putenv('SDL_MOUSEDRV', 'TSLIB') #setup mouse in pygame
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') #touchscreen as mouse

pygame.init()
pygame.mouse.set_visible(False)
time_limit = 15 #second
start_time = time.time()
code_running = True
black = 0, 0, 0
#BAIL OUT BUTTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def GPIO17_callback(channel):
    print "in interrupt 17"
    global code_running
    code_running = False

def elastic(speed1,speed2):
    tmp = [speed1[0], speed1[1]]
    #if ballrect.colliderect(ballrect2): 
    speed1[0] = speed2[0]
    speed1[1] = speed2[1]
    speed2[0] = tmp[0]
    speed2[1] = tmp[1]


GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
size = width, height = 320, 240
BLACK = 0, 0, 0
WHITE = 255,255,255
screen = pygame.display.set_mode(size)
pygame.init()
my_font = pygame.font.Font(None,30)
my_buttons = {'Start':(80, 220), 'Quit':(240, 220)}
screen.fill(BLACK) # Erase the Work space
for my_text,text_pos in my_buttons.items():
    text_surface = my_font.render(my_text,True,WHITE)
    rect = text_surface.get_rect(center=text_pos)
    screen.blit(text_surface,rect)
pygame.display.flip()
animation_running = False
paused = False
sleeptime = 0.02

size2 = width2, height2 = 320, 200
speed1 = [1, 2]
speed2 = [3, 1]
black = 0, 0, 0
ball1 = pygame.image.load("../../python_games/gem1.png")
ball2 = pygame.image.load("../../python_games/gem2.png")
balls = [ball1, ball2]
ballrect = balls[0].get_rect()
ballrect.x = 50
ballrect.y = 50

ballrect2 = balls[1].get_rect()
ballrect2.x = 150
ballrect2.y = 100
while(code_running):
    for event in pygame.event.get():
        if(event.type is pygame.MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
    
        if(event.type is pygame.MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x, y = pos
            print(x,y)
            if y > 150:
                if x > 160:
                    code_running = False
                else:

                    animation_running = True
            else: 
                pygame.draw.rect(screen, black, pygame.Rect(50, 0, 250, 120))
                pygame.display.flip()
                text_surface = my_font.render("Position = ("+str(x)+","+str(y)+")",True,WHITE)
                rect = text_surface.get_rect(center=(160, 100))
                screen.blit(text_surface,rect)
                pygame.display.flip()

        
         
        
    if animation_running:
        pygame.draw.rect(screen, black, pygame.Rect(0, 0, 320, 200))
        ballrect = ballrect.move(speed1)
        if ballrect.left < 0 or ballrect.right > width2:
            #elastic(speed1, speed2)
            speed1[0] = -speed1[0]
                    
            
        if ballrect.top < 0 or ballrect.bottom > height2:
            #elastic(speed1, speed2)
            speed1[1] = -speed1[1]
                    
        ballrect2 = ballrect2.move(speed2)
        if ballrect2.left < 0 or ballrect2.right > width2:
            #elastic(speed1, speed2)
            speed2[0] = -speed2[0]

        if ballrect2.top < 0 or ballrect2.bottom > height2:
            #elastic(speed1, speed2)
            speed2[1] = -speed2[1]

        if(ballrect2.colliderect(ballrect)):
            elastic(speed1,speed2)	
        
        screen.blit(ball1, ballrect)
        screen.blit(ball2, ballrect2)
        pygame.display.flip()
        time.sleep(sleeptime)
            
GPIO.cleanup()	