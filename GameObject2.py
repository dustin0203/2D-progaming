from pico2d import *
from math import *
import random

class Background():
    def __init__(self,name):
        self.image = load_image(name)
    def Draw(self,cameraRect):
        self.image.static_Object_draw(cameraRect)
    def GetWidth(self):
        return self.image.w
    def GetHeight(self):
        return self.image.h
    def __del__(self):
        SDL_DestroyTexture(self.image)

class Debris1():

    image = None
    BOTTOM = 1335
    remove = False
    def __init__(self,X,Y):
        if Debris1.image ==None:
            Debris1.image = load_image("debris1.png")
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        X=X+random.randint(0,400)-50
        Y=Y+random.randint(0,50)-50
        self.R = random.randint(0,360)
        self.V = random.randint(0,1)
        self.originX = self.image.w / 2
        self.originY = self.image.h / 2
        self.positionRect.x = X
        self.positionRect.y = Y
        self.positionRect.w = self.image.w
        self.positionRect.h = self.image.h
        self.gravity = 9.8;
        self.moveSpeedX = random.randint(0,400)-200
        self.moveSpeedY = random.randint(0,400)
    def Update(self,delta):
        if(self.V==0):
            self.positionRect.x =int(self.positionRect.x+((self.moveSpeedX *delta) ))
            self.moveSpeedX = self.moveSpeedX +1
        else:
            self.positionRect.x =int(self.positionRect.x-((self.moveSpeedX *delta) ))
            self.moveSpeedX = self.moveSpeedX -1
        self.positionRect.y =int(self.positionRect.y-((self.moveSpeedY *delta) ))

        self.moveSpeedY = self.moveSpeedY -self.gravity


    def Draw(self,cameraRect):
        self.image.dynamic_draw(self.positionRect,cameraRect)

    def __del__(self):
        pass

class Debris2():

    image = None
    BOTTOM = 1335
    remove = False
    def __init__(self,X,Y):
        if Debris2.image ==None:
            Debris2.image = load_image("debris2.png")
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        X=X+random.randint(0,400)-50
        Y=Y+random.randint(0,50)-50
        self.R = random.randint(0,360)
        self.V = random.randint(0,1)
        self.originX = self.image.w / 2
        self.originY = self.image.h / 2
        self.positionRect.x = X
        self.positionRect.y = Y
        self.positionRect.w = self.image.w
        self.positionRect.h = self.image.h
        self.gravity = 9.8;
        self.moveSpeedX = random.randint(0,400)-200
        self.moveSpeedY = random.randint(0,400)
    def Update(self,delta):
        if(self.V==0):
            self.positionRect.x =int(self.positionRect.x+((self.moveSpeedX *delta) ))
            self.moveSpeedX = self.moveSpeedX +1
        else:
            self.positionRect.x =int(self.positionRect.x-((self.moveSpeedX *delta) ))
            self.moveSpeedX = self.moveSpeedX -1
        self.positionRect.y =int(self.positionRect.y-((self.moveSpeedY *delta) ))

        self.moveSpeedY = self.moveSpeedY -self.gravity


    def Draw(self,cameraRect):
        self.image.dynamic_draw(self.positionRect,cameraRect)

    def __del__(self):
        pass

class Debris3():

    image = None
    BOTTOM = 1335
    remove = False
    def __init__(self,X,Y):
        if Debris3.image ==None:
            Debris3.image = load_image("debris3.png")
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        X=X+random.randint(0,400)-50
        Y=Y+random.randint(0,50)-50
        self.R = random.randint(0,360)
        self.V = random.randint(0,1)
        self.originX = self.image.w / 2
        self.originY = self.image.h / 2
        self.positionRect.x = X
        self.positionRect.y = Y
        self.positionRect.w = self.image.w
        self.positionRect.h = self.image.h
        self.gravity = 9.8;
        self.moveSpeedX = random.randint(0,400)-200
        self.moveSpeedY = random.randint(0,400)
    def Update(self,delta):
        if(self.V==0):
            self.positionRect.x =int(self.positionRect.x+((self.moveSpeedX *delta) ))
            self.moveSpeedX = self.moveSpeedX +1
        else:
            self.positionRect.x =int(self.positionRect.x-((self.moveSpeedX *delta) ))
            self.moveSpeedX = self.moveSpeedX -1
        self.positionRect.y =int(self.positionRect.y-((self.moveSpeedY *delta) ))

        self.moveSpeedY = self.moveSpeedY -self.gravity


    def Draw(self,cameraRect):
        self.image.dynamic_draw(self.positionRect,cameraRect)

    def __del__(self):
        pass



class Brokenbuilding():

    def __init__(self,X,Y):
        self.Debris= []
        self.rand= None
        self.remove=False
        for i in range(20):
            r=random.randint(0,2)
            if (r==0):
                self.Debris.append(Debris1(X,Y))
            elif (r==1):
                self.Debris.append(Debris2(X,Y))
            else:
                self.Debris.append(Debris3(X,Y))

    def Update(self,delta):
        for deb in self.Debris:
            deb.Update(delta)
            if(deb.positionRect.y>=2500):
                self.remove = True

    def Draw(self,camerRect):
        for deb in self.Debris:
            deb.Draw(camerRect)

    def __del__(self):
        del(self.Debris)


class Building():

    image = None
    BOTTOM = 1335
    LEVEL = 5
    HIT = False
    Broken = False

    def __init__(self,name,X,Y):

        if Building.image ==None:
            Building.image = load_image(name)

        self.cropRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.positionRect.x = X
        self.positionRect.y = Y
        self.cropRect.w = self.image.w
        self.cropRect.h = self.image.h

        self.frameY =int (self.cropRect.h/5)
        self.cropRect.h = int(self.frameY*self.LEVEL)

        self.frameWidth = self.positionRect.w = self.cropRect.w
        self.frameHeight = self.positionRect.h =self.cropRect.h

        self.originX = self.frameWidth / 2
        self.originY = self.frameHeight / 2

        self.gravity = 9.8/6;
        self.moveSpeed = 0



    def Update(self,delta):

        if (self.positionRect.y+self.positionRect.h <=self.BOTTOM ):
            self.positionRect.y =int(self.positionRect.y-(self.moveSpeed *delta))
            self.moveSpeed = self.moveSpeed -self.gravity
        else:
            self.moveSpeed = 0

        if (self.HIT ==True):
            self.LEVEL-=1

        if (self.LEVEL ==0):
            self.Broken= True

        self.cropRect.h = int(self.frameY*self.LEVEL)
        self.positionRect.h = self.cropRect.h




    def Draw(self,cameraRect):
        self.image.dynamic_Object_draw(self.cropRect,self.positionRect,cameraRect)

    def get_bb(self):
        return self.positionRect.x,self.positionRect.y,self.positionRect.x+self.positionRect.w,self.positionRect.y+self.positionRect.h

    def GetOriginX(self):
        return (self.positionRect.x+(self.positionRect.x /2))
    def GetOriginY(self):
        return (self.positionRect.y+(self.frameY*self.LEVEL))

    def __del__(self):
        pass

class Player():

    BASIC_STATE,JUMP_STATE,DEFENSE_STATE= 0,2,3
    ATTACK = False
    JUMP_DEFENSE = False
    BASIC_DEFENSE = False
    JUMP_UP = False
    JUMP_DOWN = False
    Collision = False
    TOP = 587
    BOTTOM = 1335

    def __init__(self,name,X,Y,frameX,frameY):
        self.image = load_image(name)
        self.cropRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.moveSpeed = 0
        self.frameCounter = 0
        self.frameWidth = 0
        self.frameHeight = 0
        self.textureWidth = 0
        self.isActive = 0
        self.originX = 0
        self.originY = 0
        self.state = self.BASIC_STATE
        self.cropRect.w = self.image.w
        self.cropRect.h = self.image.h
        self.gravity = 9.8
        self.positionRect.x = X
        self.positionRect.y = Y
        self.textureWidth = self.cropRect.w

        self.cropRect.w = int (self.cropRect.w/frameX)
        self.cropRect.h = int (self.cropRect.h/frameY)

        self.frameWidth = self.positionRect.w = self.cropRect.w
        self.frameHeight = self.positionRect.h =self.cropRect.h

        self.originX = self.frameWidth / 2
        self.originY = self.frameHeight / 2
        self.isActive = 0

    def handle_event(self, event):
        self.isActive = 1

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            self.ATTACK=True

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.BASIC_STATE,):
                if self.Collision==True:
                    self.moveSpeed = 0
                else:
                    self.moveSpeed = 800
                    self.state = self.JUMP_STATE
                    self.JUMP_UP = True


        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if self.state in (self.BASIC_STATE,):
                self.state = self.DEFENSE_STATE
                self.moveSpeed = 0
                self.BASIC_DEFENSE = True
            if self.state in (self.JUMP_STATE,):
                self.state = self.DEFENSE_STATE
                self.JUMP_DEFENSE = True

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
                self.cropRect.x = self.frameWidth
                if((self.JUMP_DOWN==True)or(self.JUMP_UP==True)):
                        self.state=self.JUMP_STATE
                else:
                        self.state=self.BASIC_STATE
                self.JUMP_DEFENSE = False
                self.BASIC_DEFENSE = False


    def Update(self,delta):



        if ( (self.state == self.JUMP_STATE)):
            self.positionRect.y =int(self.positionRect.y-(self.moveSpeed *delta))
            self.moveSpeed = self.moveSpeed -self.gravity

        if ( (self.state == self.DEFENSE_STATE)):
            if(self.JUMP_DEFENSE ==True):
                self.positionRect.y =int(self.positionRect.y-(self.moveSpeed *delta))
                self.moveSpeed = self.moveSpeed -self.gravity


        if self.GetOriginY() <=self.TOP :
                    self.JUMP_DOWN =True
                    self.JUMP_UP = False


        if self.GetOriginY() >=self.BOTTOM :
                    self.JUMP_DOWN = False
                    if(self.BASIC_DEFENSE==True):
                        self.state= self.DEFENSE_STATE
                    else:
                        self.state = self.BASIC_STATE
                    self.moveSpeed = 0

        self.cropRect.y = self.frameHeight*self.state


        if(self.isActive):
            self.frameCounter += delta

            if(self.frameCounter >= 0.2):

                if(self.ATTACK==True):
                    self.cropRect.x += self.frameWidth
                    if(self.cropRect.x>=self.textureWidth):
                        self.cropRect.x = 0
                        self.isActive = 0
                        self.ATTACK=False

                if(self.BASIC_DEFENSE==True or self.JUMP_DEFENSE==True):
                    self.frameCounter = 0
                    self.cropRect.x += self.frameWidth
                    if(self.cropRect.x>480):
                        self.cropRect.x = self.frameWidth*4

        else:
            self.frameCounter = 0
            self.cropRect.x = self.frameWidth

    def Draw(self,cameraRect):
        self.image.user_Objects_draw(self.cropRect,self.positionRect,cameraRect)

    def IntersectsWith(self,Building):

        if(self.collide(Building)) :
                SDL_SetTextureColorMod(self.image.texture, 255, 0,0)
                self.Collision = True
                self.moveSpeed = Building.moveSpeed
                if( self.ATTACK==True):
                    Building.HIT=True
                if(Building.LEVEL==0):
                    self.Collision=False
                    SDL_SetTextureColorMod(self.image.texture, 255, 255, 255);
                return True


        SDL_SetTextureColorMod(self.image.texture, 255, 255, 255);
        self.Collision = False
        Building.HIT=False
        return False



    def collide(self, Building):
        left_a,bottom_a,right_a,top_a=self.get_bb()
        left_b,bottom_b,right_b,top_b=Building.get_bb()

        if left_a>right_b:
            return False
        if right_a <left_b :
            return False
        if top_a<bottom_b :
            return False
        if bottom_a>top_b:
            return False
        return True



    def get_bb(self):
        return  self.GetOriginX()-30,self.GetOriginY()-30,self.GetOriginX()+30,self.GetOriginY()+30

    def GetOriginX(self):
        return abs((self.positionRect.x + self.originX))
    def GetOriginY(self):
        return abs((self.positionRect.y + self.originY))
    def __del__(self):
        SDL_DestroyTexture(self.image)
