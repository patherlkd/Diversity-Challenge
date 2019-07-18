import RPi.GPIO as GPIO
import DC_UI.DC_ui as DCUI
import DC_TEAM.DC_team as DCT
import DC_MODES.DC_modes as DCM
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## make two instances of teams
bteam_players = ("Einstein","Turing")
bteam_GPIOs = [18,23]
rteam_players = ("Curie","Noether")
rteam_GPIOs = [5,6]

bteam = DCT.team(2,"Blue",bteam_players,bteam_GPIOs)
rteam = DCT.team(2,"Red",rteam_players,rteam_GPIOs)


## Set button inputs
bteam.setGPIOs()
rteam.setGPIOs()

## Set keypad cols as outputs
for j in range(4):
    GPIO.setup(DCM.MCOL[j], GPIO.OUT)
    GPIO.output(DCM.MCOL[j], 1)

## Set keypad rows as inputs
for i in range(4):
    GPIO.setup(DCM.MROW[i],GPIO.IN, pull_up_down = GPIO.PUD_UP)

## Setup and initialize pygame screen object
DCdisp = DCUI.dcui(1000,500)

try:

    while(True):
        DCdisp.displayLogo()
        DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "    Score: "+str(bteam.getTotalScore()),DCUI.Blue,40,70,-50)
        DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "    Score: "+str(rteam.getTotalScore()),DCUI.Red,40,70,+50)
        DCdisp.updateDisplay()
        DCdisp.displayLogo()
        mainkey = DCM.keypadEvent()
        if DCM.DC_mode(mainkey) == "Starter for 10":
            incorrect_cnt = 0
            DCM.starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
                       
           
            
except KeyboardInterrupt:
    GPIO.cleanup()  


