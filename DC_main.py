import RPi.GPIO as GPIO #Raspberry Pi library
import DC_UI.DC_ui as DCUI #DC user interface library
import DC_TEAM.DC_team as DCT #DC team library 
import DC_MODES.DC_modes as DCM #DC modes library
import time #Time library
from time import sleep #function to sleep

## Set RPi mode to IO numbers (see Pi manual)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

## make two instances of teams
bteam_players = ("Abbot","Odekunle","Cheung","Chamberlain")
bteam_GPIOs = [18,23,24,25]
rteam_players = ("Carpineti","Boland","Jackson","Jeanne")
rteam_GPIOs = [5,6,13,19]

##Set the team name and send inputs
bteam = DCT.team(4,"Cheung",bteam_players,bteam_GPIOs)
rteam = DCT.team(4,"Jackson",rteam_players,rteam_GPIOs)

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
DCdisp = DCUI.dcui(1700,1000)

try:
    
    DCdisp.updateDisplay()
       
    d=0
    for i in range(6):
        d = i*0.1
        DCdisp.updateDisplay()
        DCdisp.displayWelcome(d,0.5)
        sleep(0.03)
    
    DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Empty_box.png",1.0,0.5,0.06)
    
    DCdisp.displayText("Diversity",DCUI.Black,100,0.4,0.15)
    DCdisp.displayText("Diversity",DCUI.Blue,100,0.395,0.15)
    
    DCdisp.displayText("Challenge",DCUI.Black,100,0.6,0.3)
    DCdisp.displayText("Challenge",DCUI.Red,100,0.595,0.3)
    DCdisp.displayText("Created by Luke Kristopher Davis",DCUI.Black,30,0.2,0.95)
    DCdisp.displayText("Press [1] to start",DCUI.Black,40,0.5,0.95)
    DCdisp.updateDisplay()
               
    start = 0
    while(not start):
        if DCM.keypadEvent() == 1:
            start = 1

    ## Begin timer
    start_time = time.time()

    ## Final Round message will occur at 50*60 seconds i.e. 50 minutes
    ENDTIME = 50*60
    
    final_round_announced = 0

    ## Main game loop
    while(True):
        current_time = time.time()
        
        
        if final_round_announced:
            DCM.decideWinner(bteam,rteam,DCdisp)
        
        if current_time - start_time >= ENDTIME and not final_round_announced:
            DCdisp.displayText("FINAL ROUND",DCUI.Red,100,0.5,0.5)
            DCdisp.updateDisplay()
            final_round_announced = 1
        
        DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "    Score: "+str(bteam.getTotalScore()),DCUI.Blue,100,0.5,0.1)
        DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "    Score: "+str(rteam.getTotalScore()),DCUI.Red,100,0.5,0.55)
        
        ## Display player pictures and names

        players = bteam.getPlayers()
        xpos = 0.2
        
        for p in players:
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_TEAM/contestants/"+p.getPlayerName()+"_DC_badge.png",0.25,xpos,0.3)
            DCdisp.displayText(p.getPlayerName(),DCUI.Blue,47,xpos,0.45)
            xpos = xpos + 0.2
        
        players = rteam.getPlayers()
        xpos = 0.2
        
        for p in players:
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_TEAM/contestants/"+p.getPlayerName()+"_DC_badge.png",0.25,xpos,0.75)
            DCdisp.displayText(p.getPlayerName(),DCUI.Red,47,xpos,0.9)
            xpos = xpos + 0.2
        
        ## Display button presses

        DCdisp.displayText("[1] Starter for 10 | [2] Picture Round | [3] Decide Winner | [*] Quit",DCUI.Blue,20, 0.5, 0.975)
        DCdisp.updateDisplay()
       

        ## Wait for keypad press
        mainkey = DCM.keypadEvent()

        ## Enter the "Starter for 10" mode
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


