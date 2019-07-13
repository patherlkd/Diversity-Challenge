import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

MKEYS = [ [1,2,3,'A'],
	      [4,5,6,'B'],
	      [7,8,9,'C'],
	      ['*',0,'#','D'] ]

def DC_mode(arg):
    switcher = {
        1: "January",
        2: "February",
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

MROW = [21,20,16,12]
MCOL = [22,27,17,4]

BTEAM = 18
RTEAM = 5

GPIO.setup(RTEAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTEAM, GPIO.IN, pull_up_down=GPIO.PUD_UP)


for j in range(4):
	GPIO.setup(MCOL[j], GPIO.OUT)
	GPIO.output(MCOL[j], 1)

for i in range(4):
	GPIO.setup(MROW[i],GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:

	while(True):
		for j in range(4):
			GPIO.output(MCOL[j],0)

			for i in range (4):   
				if GPIO.input(MROW[i]) == 0: ## Input low = pressed
					print(DC_mode(MKEYS[i][j]))
					while(GPIO.input(MROW[i]) == 0):
						pass
					

			GPIO.output(MCOL[j],1) 
except KeyboardInterrupt:
	GPIO.cleanup()	
