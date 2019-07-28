import csv
import os
import random
import pygame
import RPi.GPIO as GPIO
import DC_UI.DC_ui as DCUI

WORD_PER_LINE_LIM = 8
WORD_PER_LINE_LIM_ANS = 3

class question:
    def __init__(self):
        self.questionsfile = "DC_QUESTIONS/questions/questions.csv"
        
        self.questionsblacklist = []
        self.picquestionsblacklist = []
        self.Nquestions = 0
        self.folders = 0
        with open(self.questionsfile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                self.Nquestions +=1
        
        print("Number of questions in database: ",self.Nquestions-1)
        
    def dispQuestion(self,DCdisp,question_num):
        
        DCdisp.displayImage("/home/pi/Documents/Diversity_Challenge/DC_UI/images/Game_images/"+"Empty_box.png",1.2,0.5,0.6)
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
        category = None
        author = None
        contact = None
        
        with open(self.questionsfile) as csvfile:
           readCSV = csv.reader(csvfile, delimiter=',')
           for row in readCSV:
               if question_cnt == question_num:
                   author = row[2]
                   contact = row[3]
                   category = row[4]
                   question = row[5]
                   self.answer = row[6]
               question_cnt+=1
        
        if author =="":
            DCdisp.displayText("DC Team",DCUI.DarkGreen,50,0.3,0.95)
        else:
            DCdisp.displayText(author,DCUI.DarkGreen,50,0.3,0.95)
        
        if contact =="":
            DCdisp.displayText("Twitter: @DiversityChall" ,DCUI.Black, 50, 0.7,0.95)
        else:
            DCdisp.displayText(contact, DCUI.Black, 50, 0.7,0.95)
        
        questionwords = question.split(" ");
        
        question1 = ""
        word_cnt = 1
        total_word_cnt = 1
        
        y = 0.4
        
        for word in questionwords:
            question1 += word + " "
            if word_cnt >= WORD_PER_LINE_LIM:
                DCdisp.displayText(question1,DCUI.Black,50,0.5,y)
                y+=0.06
                question1 = ""
                word_cnt = 1
            elif total_word_cnt >= len(questionwords):
                DCdisp.displayText(question1,DCUI.Black,50,0.5,y)
                
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
       
    def dispPicQuestion(self,DCdisp,folder):
        self.picpath = "/home/pi/Documents/Diversity_Challenge/DC_QUESTIONS/questions/picture_round/"
        if self.folders == 0:
            
            for _, dirnames, filenames in os.walk(self.picpath):
                self.folders += len(dirnames)
        
        try_cnt=1
        while(folder==0):
            folder = random.choice(range(self.folders)) + 1
          
           
            if try_cnt == self.folders:
                DCdisp.displayText("NO MORE PICTURES IN DATABASE",DCUI.Red,80,0.5,0.5)
                return 0
            for i in self.picquestionsblacklist:
                if folder == i:
                    folder=0
        
            try_cnt+=1
        
        if try_cnt > 1:
            self.picquestionsblacklist.append(folder)
        
        DCdisp.displayImage(self.picpath+"question_"+str(folder)+"/image.jpg",0.7,0.5,0.5)
        print("folder num: "+str(folder))
        
        return folder
    
    def dispPicAnswer(self,DCdisp,folder):
        
        info = ""
        f = open(self.picpath+"question_"+str(folder)+"/info.txt",encoding='utf-8')
        info += f.read()
        f.close()
        
        infowords = info.split(" ");
        
        info1 = ""
        word_cnt = 1
        total_word_cnt = 1
        
        y = 0.4
        
        for word in infowords:
            info1 += word + " "
            if word_cnt >= WORD_PER_LINE_LIM_ANS:
                DCdisp.displayText(info1,DCUI.Black,70,0.5,y)
                y+=0.07
                info1 = ""
                word_cnt = 1
            elif total_word_cnt >= len(infowords):
                DCdisp.displayText(info1[:-2],DCUI.Black,70,0.5,y)
                
            word_cnt+=1
            total_word_cnt+=1
        
        
DCqu = question()