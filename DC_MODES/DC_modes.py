import RPi.GPIO as GPIO
import DC_TEAM.DC_team as DCT
import DC_UI.DC_ui as DCUI
from random import shuffle
from time import sleep

## Keys on the physical matrix keypad
MKEYS = [ [1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D'] ]

##  Keys to DC main modes
def DC_mode(arg):
    switcher = {
        1: "Starter for 10",
        2: "",
        3: "",
        'A': "",
        4: "",
        5: "",
        6: "",
        'B': "",
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

def keypadEvent():
    event = 0
    key = None
    while(event==0):
        for j in range(4):
            GPIO.output(MCOL[j],0)

            for i in range (4):
                if GPIO.input(MROW[i]) == 0: ## Input low = pressed
                    while(GPIO.input(MROW[i]) == 0):
                        pass
                    event = 1
                    key = MKEYS[i][j]
            
            GPIO.output(MCOL[j],1)
        
    return key

def starter_for_10(bteam,rteam,DCdisp,incorrect_cnt): # Start of a round
    if incorrect_cnt == 2:
        DCdisp.displayLogo()
        DCdisp.displayText("Next question",DCUI.Black,60, 50, -90)
        sleep(2)
        DCdisp.updateDisplay()
        return
    
    DCdisp.displayLogo()
    DCdisp.displayText("Starter for 10 ... ",DCUI.Black,60, 50, -90)
    DCdisp.updateDisplay()
    
    allplayers = bteam.getPlayers() + rteam.getPlayers()
    shuffle(allplayers) # Shuffle for fairness
    
    winner = None 
    
    iswinner = 0 
    while iswinner == 0: 
        for p in allplayers: 
            if(p.hasBuzzed()):
                iswinner=1
                winner=p
    
    DCdisp.displayLogo()
    DCdisp.displayText("Starter for 10 ... ",DCUI.Black,60, 50, -90)
    DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,40, 40, 0)
    DCdisp.updateDisplay()
    
    
    finished = 0
    while(finished==0):
        key = keypadEvent()
        if key == 1:
            DCdisp.displayLogo()
            DCdisp.displayText("Correct ",DCUI.Green,60, 50, +30)
            DCdisp.updateDisplay()
            winner.addTen()
            sleep(3)
            finished = 1
            
        if key == 2:
            DCdisp.displayLogo()
            DCdisp.displayText("Incorrect",DCUI.Red,60, 50, +30)
            DCdisp.updateDisplay()
            sleep(2)
            
            incorrect_cnt+=1
            
            if incorrect_cnt < 2:
                DCdisp.displayLogo()
                DCdisp.displayText("Anyone from the other team?",DCUI.Black,50, 50, 0)
                DCdisp.updateDisplay()
                sleep(1)
            
            
            
            starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
            finished = 1
            
        if key == 3:
            DCdisp.displayLogo()
            DCdisp.displayText("Incorrect (-5 for interruption)",DCUI.Red,60, 50, +30)
            DCdisp.updateDisplay()
            winner.minusFive()
            sleep(2)
            
            incorrect_cnt+=1
            
            if incorrect_cnt < 2:
                DCdisp.displayLogo()
                DCdisp.displayText("Anyone from the other team?",DCUI.Black,50, 50, 0)
                DCdisp.updateDisplay()
                sleep(1)
            
            
            
            starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
            finished = 1
            
        if key == '*':
            starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
            finished = 1   
            