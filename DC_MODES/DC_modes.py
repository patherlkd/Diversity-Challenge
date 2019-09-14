import RPi.GPIO as GPIO
import DC_TEAM.DC_team as DCT
import DC_UI.DC_ui as DCUI
import DC_QUESTIONS.DC_questions as DCQ
from random import shuffle
from time import sleep
import pygame

## Keys on the physical matrix keypad
MKEYS = [ [1,2,3,'A'],
          [4,5,6,'B'],
          [7,8,9,'C'],
          ['*',0,'#','D'] ]

##  Keys to DC main modes
def DC_mode(arg):
    switcher = {
        1: "Starter for 10",
        2: "Guess the Scientist",
        3: "Decide Winner",
        'A': "",
        4: "",
        5: "",
        6: "",
        'B': "",
        7: "",
        8: "",
        9: "",
        'C': "",
        '*':"Quit",
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

def quit():
    GPIO.cleanup()
    pygame.quit()

def decideWinner(bteam,rteam,DCdisp):
    #DCdisp.displayLogo()
    DCdisp.displayText("Diversity Challenge Champions 2019 are ... ",DCUI.Blue,75, 0.5, 0.4)
    DCdisp.updateDisplay()
    sleep(4)
    
    if bteam.getTotalScore() > rteam.getTotalScore():
        winning_team = bteam
    elif bteam.getTotalScore() == rteam.getTotalScore():
        DCdisp.displayLogo()
        DCdisp.displayText("SUDDEN DEATH",DCUI.Red,100, 0.5, 0.5)
        DCdisp.updateDisplay()
        sleep(4)
        
        i_cnt = 0
        
        while(bteam.getTotalScore() == rteam.getTotalScore()):
            starter_for_10(bteam,rteam,DCdisp,i_cnt)
        
        if bteam.getTotalScore() > rteam.getTotalScore():
            winning_team = bteam
        else:
            winning_team = rteam
    else:
        winning_team = rteam
    
    #DCdisp.displayLogo()
    DCdisp.displayText("Diversity Challenge Champions 2019 are ... ",DCUI.Blue,75, 0.5, 0.3)
    #DCdisp.displayWelcomeEmpty(0.5,0.6)
    DCdisp.displayText("#TEAM "+winning_team.getTeamName(),DCUI.DarkGreen,80, 0.5, 0.85)
    
    players = winning_team.getPlayers()
    xpos = 0.2
        
    for p in players:
        DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_TEAM/contestants/"+p.getPlayerName()+"_DC_badge.png",0.25,xpos,0.6)
        DCdisp.displayText(p.getPlayerName(),DCUI.Blue,47,xpos,0.75)
        xpos = xpos + 0.2
    
    DCdisp.updateDisplay()
    
    DCdisp.soundApplause(0)
    
    
        

def starter_for_10(bteam,rteam,DCdisp,incorrect_cnt): # Start of a round
    if incorrect_cnt == 2:
        DCdisp.displayLogo()
        DCdisp.displayText("Next question",DCUI.Black,60, 0.5, 0.5)
        DCdisp.updateDisplay()
        return
    
    
    question_num = DCQ.DCqu.dispQuestion(DCdisp,0)
    
    DCdisp.displayLogo()
    DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
    DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.3, 0.2)
    
    DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "    Score: "+str(bteam.getTotalScore()),DCUI.Blue,47,0.7,0.1)
    DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "    Score: "+str(rteam.getTotalScore()),DCUI.Red,47,0.7,0.2)
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
    
    
    Nsecs = 3;
    
    while(Nsecs >= 0):
        DCdisp.displayLogo()
        #DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.3, 0.2)
        #DCQ.DCqu.dispQuestion(DCdisp,question_num)
        if winner.getTeamName() == bteam.getTeamName():
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Blue,80, 0.495, 0.8)
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.8)
        
        else:
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Red,80, 0.495, 0.8)
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.8)
        
        DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_TEAM/contestants/"+winner.getPlayerName()+"_DC_badge.png",0.4,0.5,0.5)
    
        DCdisp.displayText(str(Nsecs),DCUI.Red,100,0.5,0.1)
    
        DCdisp.updateDisplay()
    
        sleep(1)
        Nsecs -= 1
    
    DCdisp.displayLogo()
    DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
    DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.3, 0.2)
    DCQ.DCqu.dispQuestion(DCdisp,question_num)
    if winner.getTeamName() == bteam.getTeamName():
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Blue,80, 0.495, 0.8)
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.8)
    else:
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Red,80, 0.495, 0.8)
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.8)
        
    DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_TEAM/contestants/"+winner.getPlayerName()+"_DC_badge.png",0.3,0.8,0.15)        

    DCdisp.displayText("[A] Display Answer",DCUI.Blue,20, 0.1, 0.95)
    DCdisp.updateDisplay()
    
    key = '0'
    while(key != 'A'):
        key = keypadEvent()
            
    DCdisp.displayLogo()
    DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
    DCdisp.displayText("Starter for 10",DCUI.Black,60, 0.3, 0.2)
    DCQ.DCqu.dispAnswer(DCdisp)
    DCdisp.displayText("[1] Correct [2] Incorrect [3] Incorrect Interruption [*] Restart starter for 10",DCUI.Blue,20, 0.5, 0.95)
    DCdisp.updateDisplay()
    finished = 0
    correct_ans = 0
    
    while(finished==0):
        key = keypadEvent()
        if key == 1:
            DCdisp.displayLogo()
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Fire.png",0.2,0.1,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Correct.png",0.4,0.5,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Fire.png",0.2,0.9,0.5)
            DCdisp.displayText("(+10 points)",DCUI.Green,100, 0.5, 0.8)
            DCdisp.updateDisplay()
            winner.addTen()
            sleep(3)
            finished = 1
            correct_ans = 1
            
        if key == 2:
            DCdisp.displayLogo()
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_sad.png",0.2,0.1,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Incorrect.png",0.4,0.5,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_sad.png",0.2,0.9,0.5)
            DCdisp.updateDisplay()
            sleep(2)
            
            incorrect_cnt+=1
            
            if incorrect_cnt < 2:
                DCdisp.displayLogo()
                if winner.getTeamName() == bteam.getTeamName():
                    DCdisp.displayText("Starter for 10 just for #TEAM "+rteam.getTeamName(),DCUI.Red,60, 0.5, 0.5)
                else:
                    DCdisp.displayText("Starter for 10 just for #TEAM "+bteam.getTeamName(),DCUI.Blue,60, 0.5, 0.5)
                DCdisp.updateDisplay()
                sleep(1.5)
            
            
            if winner.getTeamName() == bteam.getTeamName():
                starter_for_10(rteam,rteam,DCdisp,incorrect_cnt)
            else:
                starter_for_10(bteam,bteam,DCdisp,incorrect_cnt)
            finished = 1
            
        if key == 3:
            DCdisp.displayLogo()
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_shushing.png",0.2,0.1,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Incorrect.png",0.4,0.5,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_dizzy.png",0.2,0.9,0.5)
            DCdisp.displayText("(-5 points for interruption)",DCUI.Red,60, 0.5, 0.9)
            DCdisp.updateDisplay()
            winner.minusFive()
            sleep(2)
            
            incorrect_cnt+=1
            
            if incorrect_cnt < 2:
                DCdisp.displayLogo()
                if winner.getTeamName() == bteam.getTeamName():
                    DCdisp.displayText("Starter for 10 just for #TEAM "+rteam.getTeamName(),DCUI.Red,60, 0.5, 0.5)
                else:
                    DCdisp.displayText("Starter for 10 just for #TEAM "+bteam.getTeamName(),DCUI.Blue,60, 0.5, 0.5)
                DCdisp.updateDisplay()
                sleep(2.5)
            
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
        DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCdisp.displayText("#TEAM "+team.getTeamName()+ "    Score: "+str(team.getTotalScore()),DCUI.DarkGreen,47,0.7,0.1)
        DCdisp.updateDisplay()
        sleep(2)
        
        question_num = DCQ.DCqu.dispQuestion(DCdisp,0)
        DCdisp.displayLogo()
        DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCdisp.displayText("#TEAM "+team.getTeamName()+ "    Score: "+str(team.getTotalScore()),DCUI.DarkGreen,47,0.7,0.1)
        DCdisp.updateDisplay()
    
        winner = None 
    
        iswinner = 0 
        while iswinner == 0: 
            for p in team.getPlayers(): 
                if(p.hasBuzzed()):
                    DCdisp.soundBuzz(0)
                    iswinner=1
                    winner=p
    
        
        Nsecs = 5
        
        while(Nsecs >= 0):
            DCdisp.displayLogo()
            DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
            DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
            DCdisp.displayText("#TEAM "+team.getTeamName()+ "    Score: "+str(team.getTotalScore()),DCUI.DarkGreen,47,0.7,0.1)
            #DCQ.DCqu.dispQuestion(DCdisp,question_num)
       
            DCdisp.displayText("  #TEAM "+winner.getTeamName(),DCUI.DarkGreen,80, 0.495, 0.8)
            DCdisp.displayText("  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.8)
            DCdisp.displayText(str(Nsecs),DCUI.Red,100,0.5,0.5)
    
            DCdisp.updateDisplay()
    
            sleep(1)
            Nsecs -= 1
    
        DCdisp.displayLogo()
        DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCdisp.displayText("#TEAM "+team.getTeamName()+ "    Score: "+str(team.getTotalScore()),DCUI.DarkGreen,47,0.7,0.1)
        DCQ.DCqu.dispQuestion(DCdisp,question_num)
        #DCdisp.displayText("  #TEAM "+winner.getTeamName(),DCUI.DarkGreen,80, 0.495, 0.8)
        #DCdisp.displayText("  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.8)
        DCdisp.displayText("[A] Display Answer",DCUI.Blue,20, 0.07, 0.96)
        DCdisp.updateDisplay()
    
        
        key = '0'
        while(key != 'A'):
            key = keypadEvent()
        
        DCdisp.displayLogo()
        DCdisp.displayText("Questions remaining: "+str(DCQ.DCqu.getRemaining()),DCUI.Red,40,0.2,0.05)
        DCdisp.displayText("Bonus Round",DCUI.Black,60, 0.5, 0.2)
        DCdisp.displayText("#TEAM "+team.getTeamName()+ "    Score: "+str(team.getTotalScore()),DCUI.DarkGreen,47,0.7,0.05)
        DCQ.DCqu.dispAnswer(DCdisp)
        DCdisp.displayText("[1] Correct [2] Incorrect [*] Start another bonus round question",DCUI.Blue,20, 0.5, 0.95)
        DCdisp.updateDisplay()
        
        finished = 0
    
        while(finished==0):
            key = keypadEvent()
            if key == 1:
                DCdisp.displayLogo()
                DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Fire.png",0.2,0.1,0.5)
                DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Correct.png",0.4,0.5,0.5)
                DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Fire.png",0.2,0.9,0.5)
                DCdisp.displayText("(+5 points)",DCUI.Green,100, 0.5, 0.8)
               
                DCdisp.updateDisplay()
                winner.addFive()
                sleep(3)
                finished = 1
                
                question_count +=1 
            
            if key == 2:
                DCdisp.displayLogo()
                DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_sad.png",0.2,0.1,0.5)
                DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Incorrect.png",0.4,0.5,0.5)
                DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_sad.png",0.2,0.9,0.5)
               
                DCdisp.updateDisplay()
                sleep(2)
            
                finished = 1
                
                question_count += 1
            
            if key == '*':
                finished = 1
    
def pictureRound(bteam,rteam,DCdisp,roundnum):
    
    if roundnum>=2:
        return 2
    
    DCdisp.displayLogo()
    DCdisp.displayText("Who are they?",DCUI.Black,60, 0.3, 0.1)
   
    DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "  Score: "+str(bteam.getTotalScore()),DCUI.Blue,47,0.7,0.05)
    DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "  Score: "+str(rteam.getTotalScore()),DCUI.Red,47,0.7,0.1)
    picquestionnumber = DCQ.DCqu.dispPicQuestion(DCdisp,0)
    DCdisp.displayText("Pictures remaining: "+str(DCQ.DCqu.getRemainingPics()),DCUI.Red,40,0.2,0.05)
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
    
    Nsecs = 3
    
    while(Nsecs >= 0):
    
        DCdisp.displayLogo()
        #DCdisp.displayText("Who are they?",DCUI.Black,60, 0.3, 0.1)
    
        if winner.getTeamName() == bteam.getTeamName():
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Blue,80, 0.495, 0.9)
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.9)
        else:
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Red,80, 0.495, 0.9)
            DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.9)
        
       # DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "  Score: "+str(bteam.getTotalScore()),DCUI.Blue,50,0.8,0.05)
       # DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "  Score: "+str(rteam.getTotalScore()),DCUI.Red,50,0.8,0.1)
        
        DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_TEAM/contestants/"+winner.getPlayerName()+"_DC_badge.png",0.4,0.5,0.5)
        
        DCdisp.displayText(str(Nsecs),DCUI.Red,100,0.5,0.1)
        
        
        
        #DCQ.DCqu.dispPicQuestion(DCdisp,picquestionnumber)
        DCdisp.updateDisplay()
    
        sleep(1)
        Nsecs -= 1
    
    DCdisp.displayLogo()
    DCdisp.displayText("Pictures remaining: "+str(DCQ.DCqu.getRemainingPics()),DCUI.Red,40,0.2,0.05)
    DCdisp.displayText("Who are they?",DCUI.Black,60, 0.3, 0.1)
    
    if winner.getTeamName() == bteam.getTeamName():
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Blue,80, 0.495, 0.9)
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.9)
    else:
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Red,80, 0.495, 0.9)
        DCdisp.displayText(winner.getPlayerName()+"  #TEAM "+winner.getTeamName(),DCUI.Black,80, 0.5, 0.9)
        
    DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "  Score: "+str(bteam.getTotalScore()),DCUI.Blue,47,0.7,0.05)
    DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "  Score: "+str(rteam.getTotalScore()),DCUI.Red,47,0.7,0.1)
    DCdisp.displayText("[A] Display Answer",DCUI.Blue,20, 0.9, 0.95)
    DCQ.DCqu.dispPicQuestion(DCdisp,picquestionnumber)
    DCdisp.updateDisplay()
    
    key = 'O'
    while(key != 'A'):
        key=keypadEvent()
    
    DCdisp.displayLogo()
    DCdisp.displayText("Who are they?",DCUI.Black,60, 0.3, 0.1)
    DCdisp.displayText("[1] Correct [2] Incorrect [*] Start another Who are they? question",DCUI.Blue,20, 0.5, 0.95)
    DCdisp.displayText("#TEAM "+bteam.getTeamName()+ "  Score: "+str(bteam.getTotalScore()),DCUI.Blue,47,0.7,0.05)
    DCdisp.displayText("#TEAM "+rteam.getTeamName()+ "  Score: "+str(rteam.getTotalScore()),DCUI.Red,47,0.7,0.1)
    DCQ.DCqu.dispPicAnswer(DCdisp,picquestionnumber)
    DCdisp.updateDisplay()
    
    finished=0
    
    while(finished==0):
        key = keypadEvent()
        if key == 1:
            DCdisp.displayLogo()
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Fire.png",0.2,0.1,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Correct.png",0.4,0.5,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Fire.png",0.2,0.9,0.5)
            DCdisp.displayText("(+10 points)",DCUI.Green,100, 0.5, 0.8)
          
            DCdisp.updateDisplay()
            winner.addTen()
            sleep(3)
            finished = 1
                
            roundnum +=1
            
            pictureRound(bteam,rteam,DCdisp,roundnum)
            
        if key == 2:
            DCdisp.displayLogo()
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_sad.png",0.2,0.1,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Incorrect.png",0.4,0.5,0.5)
            DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Face_sad.png",0.2,0.9,0.5)
            DCdisp.updateDisplay()
            sleep(2)
        
            finished = 1
                
            roundnum += 1
                
            pictureRound(bteam,rteam,DCdisp,roundnum)
            
        if key == '*':
            finished = 1
            pictureRound(bteam,rteam,DCdisp,roundnum)
