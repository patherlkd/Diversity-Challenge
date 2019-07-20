import RPi.GPIO as GPIO
import DC_TEAM.DC_team as DCT
import DC_UI.DC_ui as DCUI
import DC_QUESTIONS.DC_questions as DCQ
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
        DCdisp.displayText("Next question",DCUI.Black,60, 0.5, 0.5)
        DCdisp.updateDisplay()
        sleep(2)
        return
    
    question_num = DCQ.DCqu.dispQuestion(DCdisp,0)
    
    DCdisp.displayLogo()
    DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.5, 0.2)
   
    DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "    Score: "+str(bteam.getTotalScore()),DCUI.Blue,80,0.5,0.7)
    DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "    Score: "+str(rteam.getTotalScore()),DCUI.Red,80,0.5,0.9)
    DCdisp.updateDisplay()
    
    allplayers = bteam.getPlayers() + rteam.getPlayers()
    shuffle(allplayers) # Shuffle for fairness
    
    winner = None 
    
    iswinner = 0 
    while iswinner == 0: 
        for p in allplayers: 
            if(p.hasBuzzed()):
                DCdisp.soundBuzz(0)
                iswinner=1
                winner=p
    
    DCdisp.displayLogo()
    DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.5, 0.2)
    DCQ.DCqu.dispQuestion(DCdisp,question_num)
    if winner.getTeamName() == bteam.getTeamName():
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.7)
    else:
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.7)
    
    DCdisp.updateDisplay()
    
    sleep(3)
    
    DCdisp.displayLogo()
    DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.5, 0.2)
    DCQ.DCqu.dispQuestion(DCdisp,question_num)
    if winner.getTeamName() == bteam.getTeamName():
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.7)
    else:
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.7)
    DCdisp.displayText("[A] Display Answer",DCUI.Blue,20, 0.5, 0.95)
    DCdisp.updateDisplay()
    
    if keypadEvent() == 'A':
        DCdisp.displayLogo()
        DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.5, 0.2)
        DCQ.DCqu.dispAnswer(DCdisp)
        DCdisp.displayText("[1] Correct [2] Incorrect [3] Incorrect Interruption [*] Restart starter for 10",DCUI.Blue,20, 0.5, 0.95)
        DCdisp.updateDisplay()
    finished = 0
    correct_ans = 0
    
    while(finished==0):
        key = keypadEvent()
        if key == 1:
            DCdisp.displayLogo()
            DCdisp.displayText("Correct (+10 points)",DCUI.Green,100, 0.5, 0.5)
            DCdisp.updateDisplay()
            winner.addTen()
            sleep(3)
            finished = 1
            correct_ans = 1
            
        if key == 2:
            DCdisp.displayLogo()
            DCdisp.displayText("Incorrect",DCUI.Red,100,0.5,0.5)
            DCdisp.updateDisplay()
            sleep(2)
            
            incorrect_cnt+=1
            
            if incorrect_cnt < 2:
                DCdisp.displayLogo()
                if winner.getTeamName() == bteam.getTeamName():
                    DCdisp.displayText("Starter for 10 just for "+rteam.getTeamName(),DCUI.Red,60, 0.5, 0.5)
                else:
                    DCdisp.displayText("Starter for 10 just for "+bteam.getTeamName(),DCUI.Blue,60, 0.5, 0.5)
                DCdisp.updateDisplay()
                sleep(1.5)
            
            
            if winner.getTeamName() == bteam.getTeamName():
                starter_for_10(rteam,rteam,DCdisp,incorrect_cnt)
            else:
                starter_for_10(bteam,bteam,DCdisp,incorrect_cnt)
            finished = 1
            
        if key == 3:
            DCdisp.displayLogo()
            DCdisp.displayText("Incorrect (-5 points for interruption)",DCUI.Red,60, 0.5, 0.5)
            DCdisp.updateDisplay()
            winner.minusFive()
            sleep(2)
            
            incorrect_cnt+=1
            
            if incorrect_cnt < 2:
                DCdisp.displayLogo()
                if winner.getTeamName() == bteam.getTeamName():
                    DCdisp.displayText("Start for 10 just for "+rteam.getTeamName(),DCUI.Red,50, 0.5, 0.5)
                else:
                    DCdisp.displayText("Start for 10 just for "+bteam.getTeamName(),DCUI.Blue,50, 0.5, 0.5)
                DCdisp.updateDisplay()
                sleep(1.5)
            
            if winner.getTeamName() == bteam.getTeamName():
                starter_for_10(rteam,rteam,DCdisp,incorrect_cnt)
            else:
                starter_for_10(bteam,bteam,DCdisp,incorrect_cnt)
            finished = 1
            
        if key == '*':
            starter_for_10(bteam,rteam,DCdisp,incorrect_cnt)
            finished = 1
            
    if correct_ans == 1:
        if winner.getTeamName() == bteam.getTeamName():
            bonusRound(bteam,DCdisp)  
        else:
            bonusRound(rteam,DCdisp)
    else:
        pass

def bonusRound(team,DCdisp):
    
    question_count = 0
    while(question_count < 3):
        DCdisp.displayLogo()
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCdisp.updateDisplay()
        sleep(2)
        
        question_num = DCQ.DCqu.dispQuestion(DCdisp,0)
        DCdisp.displayLogo()
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCdisp.updateDisplay()
    
        winner = None 
    
        iswinner = 0 
        while iswinner == 0: 
            for p in team.getPlayers(): 
                if(p.hasBuzzed()):
                    DCdisp.soundBuzz(0)
                    iswinner=1
                    winner=p
    
    
        DCdisp.displayLogo()
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCQ.DCqu.dispQuestion(DCdisp,question_num)
       
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.7)
       
    
        DCdisp.updateDisplay()
    
        sleep(3)
    
        DCdisp.displayLogo()
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCQ.DCqu.dispQuestion(DCdisp,question_num)
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.7)
        DCdisp.displayText("[A] Display Answer",DCUI.Blue,20, 0.5, 0.95)
        DCdisp.updateDisplay()
    
        if keypadEvent() == 'A':
            DCdisp.displayLogo()
            DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
            DCQ.DCqu.dispAnswer(DCdisp)
            DCdisp.displayText("[1] Correct [2] Incorrect [*] Start another bonus round question",DCUI.Blue,20, 0.5, 0.95)
        DCdisp.updateDisplay()
        
        finished = 0
    
        while(finished==0):
            key = keypadEvent()
            if key == 1:
                DCdisp.displayLogo()
                DCdisp.displayText("Correct (+5 points)",DCUI.Green,100, 0.5, 0.5)
                DCdisp.updateDisplay()
                winner.addFive()
                sleep(3)
                finished = 1
                
                question_count +=1 
            
            if key == 2:
                DCdisp.displayLogo()
                DCdisp.displayText("Incorrect",DCUI.Red,100,0.5,0.5)
                DCdisp.updateDisplay()
                sleep(2)
            
                finished = 1
                
                question_count += 1
            
            if key == '*':
                finished = 1
    
