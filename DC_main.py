import RPi.GPIO as GPIO
import DC_UI.DC_ui as DCUI
from time import sleep

GPIO.setmode(GPIO.BCM)

## Keys on the physical matrix keypad
MKEYS = [ [1,2,3,'A'],
	      [4,5,6,'B'],
	      [7,8,9,'C'],
	      ['*',0,'#','D'] ]

##  Keys to DC main modes
def DC_mode(arg):
    switcher = {
        1: "Starter for 10",
        2: "Bonus round",
        3: "March",
        'A': "April",
        4: "May",
        5: "June",
        6: "July",
        'B': "August",
	7: "",
	8: "",
	9: "",
	'C': "",
	'*':"",
	0:"",
	'#':"",
	'D':""
    }
    return switcher.get(arg, "mode_err")

## GPIO pins for matrix keyboard
MROW = [21,20,16,12]
MCOL = [22,27,17,4]

## GPIO pins for the dome buttons
BTEAM = [18,23]
RTEAM = [5,6]

## Set button inputs
for i in range(2):
	GPIO.setup(BTEAM[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(RTEAM[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)

## Set keypad cols as outputs
for j in range(4):
	GPIO.setup(MCOL[j], GPIO.OUT)
	GPIO.output(MCOL[j], 1)

## Set keypad rows as inputs
for i in range(4):
	GPIO.setup(MROW[i],GPIO.IN, pull_up_down = GPIO.PUD_UP)

## Setup and initialize pygame screen
DCUI.setup(1000,500)

try:

	while(True):
		for j in range(4):
			GPIO.output(MCOL[j],0)

			for i in range (4):
				if GPIO.input(MROW[i]) == 0: ## Input low = pressed
					print("Entering Mode: ",DC_mode(MKEYS[i][j]))
					while(GPIO.input(MROW[i]) == 0):
						pass
					if DC_mode(MKEYS[i][j]) == "Starter for 10":
						winner = 0
						while(winner==0):
							if GPIO.input(BTEAM[0]) == 0:
								print("Blue Team: Player 1")
								winner = 1
							if GPIO.input(BTEAM[1]) == 0:
								print("Blue Team: Player 2")
								winner = 1
							if GPIO.input(RTEAM[0]) == 0:
								print("Red Team: Player 1")
								winner = 1
							if GPIO.input(RTEAM[1]) == 0:
								print("Red Team: Player 2")
								winner = 1

			GPIO.output(MCOL[j],1) 
except KeyboardInterrupt:
	GPIO.cleanup()	


