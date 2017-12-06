from pico2d import *

class Building1():

    image = None
    BOTTOM = 1335
    LEVEL = 5
    HP = 1
    SCORE = 10
    HIT = False
    Broken = False
    SKILL = False
    Broken_on = False

    def __init__(self,X,Y):

        if Building1.image == None:
            Building1.image = load_image("building1.png")

        self.cropRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.positionRect.x = X
        self.positionRect.y = Y
        self.cropRect.w = self.image.w
        self.cropRect.h = self.image.h

        self.frameY = int(self.cropRect.h/5)
        self.cropRect.h = int(self.frameY * self.LEVEL)

        self.frameWidth = self.positionRect.w = self.cropRect.w
        self.frameHeight = self.positionRect.h =self.cropRect.h

        self.originX = self.frameWidth / 2
        self.originY = self.frameHeight / 2

        self.gravity = 9.8/20;
        self.moveSpeed = 0

    def Update(self,delta):

        if (self.positionRect.y+self.positionRect.h < self.BOTTOM):
            self.positionRect.y = int(self.positionRect.y - (self.moveSpeed * delta))
            self.moveSpeed = self.moveSpeed - self.gravity
        else:
            self.moveSpeed = 0

        if (self.HIT == True):
            self.HP -= 1
            self.HIT = False

        if (self.HP == 0):
            self.LEVEL -= 1
            self.HP = 1
            self.Broken_on = True

        if (self.LEVEL == 0):
            self.Broken= True

        self.cropRect.h = int(self.frameY * self.LEVEL)
        self.positionRect.h = self.cropRect.h

    def Draw(self,cameraRect):
        self.image.dynamic_Object_draw(self.cropRect,self.positionRect,cameraRect)

    def get_bb(self):
        return self.positionRect.x,self.positionRect.y,self.positionRect.x+self.positionRect.w,self.positionRect.y+self.positionRect.h

    def GetOriginX(self):
        return (self.positionRect.x+(self.positionRect.x / 2))

    def GetOriginY(self):
        return (self.positionRect.y + (self.frameY * self.LEVEL))

    def __del__(self):
        pass
