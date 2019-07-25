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
    
    d=0
    for i in range(6):
        d = i*0.1
        DCdisp.updateDisplay()
        DCdisp.displayWelcome(d,0.5)
        sleep(0.03)
    
    DCdisp.displayText("Diversity",DCUI.Black,100,0.4,0.15)
    DCdisp.displayText("Diversity",DCUI.Blue,100,0.395,0.15)
    
    DCdisp.displayText("Challenge",DCUI.Black,100,0.6,0.3)
    DCdisp.displayText("Challenge",DCUI.Red,100,0.595,0.3)
    DCdisp.displayText("Press [1] to start",DCUI.Black,40,0.5,0.95)
    DCdisp.updateDisplay()
         
    start = 0
      
    while(not start):
        if DCM.keypadEvent() == 1:
            start = 1
    
    while(True):
       # DCdisp.displayLogo()
        DCdisp.displayWelcomeEmpty(0.5,0.5)
        DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "    Score: "+str(bteam.getTotalScore()),DCUI.Blue,100,0.5,0.2)
        DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "    Score: "+str(rteam.getTotalScore()),DCUI.Red,100,0.5,0.8)
        DCdisp.displayText("[1] Starter for 10 | [2] Picture Round | [3] Decide Winner | [*] Quit",DCUI.Blue,20, 0.5, 0.95)
        DCdisp.updateDisplay()
        DCdisp.displayLogo()
        mainkey = DCM.keypadEvent()
        if DCM.DC_mode(mainkey) == "Starter for 10":
            incorrect_cnt = 0
            DCM.starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
            
        if DCM.DC_mode(mainkey) == "Guess the Scientist":
            DCM.pictureRound(bteam,rteam,DCdisp,0)
        
        if DCM.DC_mode(mainkey) == "Decide Winner":
            DCM.decideWinner(bteam,rteam,DCdisp)
        
        if DCM.DC_mode(mainkey) == "Quit":
            DCM.quit()
           
            
except KeyboardInterrupt:
    GPIO.cleanup()  


