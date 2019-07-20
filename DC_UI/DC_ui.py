import pygame
from time import sleep

Black = [0, 0, 0]
White = [255,255,255]
Green = [0,255,0]
DarkGreen = [0,102,0]
Blue = [0,0,180]
Red = [255,0,0]

class dcui:

    def __init__(self,width,height):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.disp_size = width, height
        
        self.DClogoimage = pygame.image.load('DC_UI/images/DC_icon.png')
        self.Mainimage = pygame.image.load('DC_UI/images/diversitychallenge_mainimage.png')
        self.Mainimageempty = pygame.image.load('DC_UI/images/diversitychallenge_mainimage_empty.png')
        
        self.DClogoimage = pygame.transform.scale(self.DClogoimage, (int(self.DClogoimage.get_width()/5),int(self.DClogoimage.get_height()/5)))
        self.Mainimage = pygame.transform.scale(self.Mainimage, (int(self.Mainimage.get_width()/12),int(self.Mainimage.get_height()/12)))
        self.Mainimageempty = pygame.transform.scale(self.Mainimageempty, (int(self.Mainimageempty.get_width()),int(self.Mainimageempty.get_height())))
        
        pygame.display.set_caption('Diversity Challenge')
        self.main_display = pygame.display.set_mode(self.disp_size) ## rset surface object
        self.main_display.fill(White)
        
    def getScreenWidth(self):
        return self.width
    
    def getScreenHeight(self):
        return self.height
    
    def place(self,objwidth,objheight,xfrac,yfrac):
        if xfrac < 0.0:
            xfrac = 0.0
        elif xfrac > 1.0:
            xfrac = 1.0
            
        if yfrac < 0.0:
            yfrac = 0.0
        elif yfrac > 1.0:
            yfrac = 1.0
       
        xpos = xfrac*self.width - objwidth*0.5
        ypos = yfrac*self.height - objheight*0.5
        
        position = (int(xpos),int(ypos))
        
        return position
        
    def updateDisplay(self):
        pygame.display.update()
        self.main_display.fill(White)
        
    def displayLogo(self):
        self.main_display.blit(self.DClogoimage,(0,+20))
    
    def displayWelcome(self,x,y):
        w = self.Mainimage.get_size()[0]
        h = self.Mainimage.get_size()[1]
        self.main_display.blit(self.Mainimage,self.place(w,h,x,y))
        
    def displayWelcomeEmpty(self,x,y):
        w = self.Mainimageempty.get_size()[0]
        h = self.Mainimageempty.get_size()[1]
        self.main_display.blit(self.Mainimageempty,self.place(w,h,x,y))
        
    def text_objects(self,text, font,color):
        textsurface = font.render(text,True,color)
        return textsurface, textsurface.get_rect()
    
    def displayText(self,text,color,fontsize,x,y):
        textpy = pygame.font.Font(pygame.font.get_default_font(),fontsize)
        textsurf, textrect = self.text_objects(text, textpy, color)
        textrect.center = self.place(0,0,x,y)
        self.main_display.blit(textsurf,textrect)
        
    def soundBuzz(self,dur_secs):
        snd = pygame.mixer.Sound("DC_UI/sounds/Buzz.wav")
        pygame.mixer.Sound.play(snd)
        sleep(dur_secs)
        
    def soundApplause(self,rep):
        snd = pygame.mixer.music.load("DC_UI/sounds/Applause.mp3")
        pygame.mixer.music.play(rep)
        while pygame.mixer.music.get_busy(): 
            pygame.time.Clock().tick(10)
            
     
        
        

