import pygame

Black = [0, 0, 0]
White = [255,255,255]
Green = [0,255,0]
Blue = [0,0,180]
Red = [255,0,0]

class dcui:

    def __init__(self,width,height):
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.disp_size = width, height
        
        self.DClogoimage = pygame.image.load('DC_UI/images/DC_icon.png')
        self.DClogoimage = pygame.transform.scale(self.DClogoimage, (int(self.DClogoimage.get_width()/5),int(self.DClogoimage.get_height()/5)))
        
        pygame.display.set_caption('Diversity Challenge')
        self.main_display = pygame.display.set_mode(self.disp_size) ## rset surface object
        self.main_display.fill(White)
        
    def updateDisplay(self):
        pygame.display.update()
        self.main_display.fill(White)
        
    def displayLogo(self):
        self.main_display.blit(self.DClogoimage,(0,0))
    
    def text_objects(self,text, font,color):
        textsurface = font.render(text,True,color)
        return textsurface, textsurface.get_rect()
    
    def displayText(self,text,color,fontsize,x,y):
        textpy = pygame.font.Font(pygame.font.get_default_font(),fontsize)
        textsurf, textrect = self.text_objects(text, textpy, color)
        xpos = int(self.width/2 + x)
        ypos = int(self.height/2 + y)
        textrect.center = ((xpos),(ypos))
        self.main_display.blit(textsurf,textrect)
       
        
        

