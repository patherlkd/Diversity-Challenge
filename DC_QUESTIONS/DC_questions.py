import csv
import os
import random
import pygame
import RPi.GPIO as GPIO
import DC_UI.DC_ui as DCUI

WORD_PER_LINE_LIM = 12
WORD_PER_LINE_LIM_ANS = 3

class question:
    def __init__(self):
        self.questionsfile = "DC_QUESTIONS/questions/questions.csv"
        
        self.questionsblacklist = []
        self.Nquestions = 0 
        with open(self.questionsfile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                self.Nquestions +=1
        
        print("Number of questions in database: ",self.Nquestions-1)
        
    def dispQuestion(self,DCdisp,question_num):

        try_cnt=1
        while(question_num==0):
            question_num = random.choice(range(self.Nquestions))
          
           
            if try_cnt == self.Nquestions:
                DCdisp.displayText("NO MORE QUESTIONS IN DATABASE",DCUI.Red,100,0.5,0.5)
                return 0
            for i in self.questionsblacklist:
                if question_num == i:
                    question_num=0
        
            try_cnt+=1
            
        self.questionsblacklist.append(question_num)
        question_cnt = 0
        
        question = None
        with open(self.questionsfile) as csvfile:
           readCSV = csv.reader(csvfile, delimiter=',')
           for row in readCSV:
               if question_cnt == question_num:
                   question = row[5]
                   self.answer = row[6]
               question_cnt+=1
        
        questionwords = question.split(" ");
        
        question1 = ""
        word_cnt = 1
        total_word_cnt = 1
        
        y = 0.4
        
        for word in questionwords:
            question1 += word + " "
            if word_cnt >= WORD_PER_LINE_LIM:
                DCdisp.displayText(question1,DCUI.Black,40,0.5,y)
                y+=0.05
                question1 = ""
                word_cnt = 1
            elif total_word_cnt >= len(questionwords):
                DCdisp.displayText(question1,DCUI.Black,40,0.5,y)
                
            word_cnt+=1
            total_word_cnt+=1
        return question_num
    
    def dispAnswer(self,DCdisp):
        answerwords = self.answer.split(" ");
        
        ans1 = ""
        word_cnt = 1
        total_word_cnt = 1
        
        y = 0.45
        
        for word in answerwords:
            ans1 += word + " "
            if word_cnt >= WORD_PER_LINE_LIM_ANS:
                DCdisp.displayText(ans1,DCUI.DarkGreen,80,0.5,y)
                y+=0.1
                ans1 = ""
                word_cnt = 1
            elif total_word_cnt >= len(answerwords):
                DCdisp.displayText(ans1,DCUI.DarkGreen,80,0.5,y)
                
            word_cnt+=1
            total_word_cnt+=1
       

DCqu = question()