import RPi.GPIO as GPIO
import DC_UI.DC_ui as DCUI
import DC_TEAM.DC_team as DCT
import DC_MODES.DC_modes as DCM
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## make two instances of teams
bteam_players = ("Player 1","Player 2","Player 3")
bteam_GPIOs = [18,23,24]
rteam_players = ("Player 1","Player 2","Player 3")
rteam_GPIOs = [5,6,13]

bteam = DCT.team(3,"Blue",bteam_players,bteam_GPIOs)
rteam = DCT.team(3,"Red",rteam_players,rteam_GPIOs)

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
DCdisp = DCUI.dcui(1776,1000)

try:
    
    DCdisp.updateDisplay()
    
    
    for i in range(6):
        d = i*0.1
        DCdisp.updateDisplay()
        DCdisp.displayWelcome(d,0.5)
        sleep(0.03)
        
    DCdisp.displayText("Press [1] to start",DCUI.Blue,50,0.5,0.9)
    DCdisp.updateDisplay()
         
    start = 0
      
    while(not start):
        if DCM.keypadEvent() == 1:
            start = 1
    
    
    while(True):
        DCdisp.displayLogo()
        DCdisp.displayWelcome(0.5,0.5)
        DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "    Score: "+str(bteam.getTotalScore()),DCUI.Blue,100,0.5,0.2)
        DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "    Score: "+str(rteam.getTotalScore()),DCUI.Red,100,0.5,0.8)
        DCdisp.updateDisplay()
        DCdisp.displayLogo()
        mainkey = DCM.keypadEvent()
        if DCM.DC_mode(mainkey) == "Starter for 10":
            incorrect_cnt = 0
            DCM.starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
                       
           
            
except KeyboardInterrupt:
    GPIO.cleanup()  


