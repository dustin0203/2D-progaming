from pico2d import *
from math import *
import random
import json
import os

class Player():

    image = None
    skill_image = None
    slash_image = None

    BASIC_STATE, JUMP_STATE, DEFENSE_STATE= 0, 2, 3
    SKILL = False
    ATTACK = False
    DEFENSE = False
    DEFENSE_ON = False
    JUMP_DEFENSE = False
    BASIC_DEFENSE = False
    JUMP_UP = False
    JUMP_DOWN = False
    Collision = False

    TOP = 587
    BOTTOM = 1335

    HP = 3
    DAMAGE = True
    SKILL_value = 0
    DEFENSE_value = 0
    HIT = False
    SCORE = 0

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self,X,Y):

        #self.image = load_image(name)
        if Player.image == None:
            Player.image = load_image("player.png")

        if Player.skill_image == None:
            Player.skill_image = load_image("skill_image.png")

        if Player.slash_image == None:
            Player.slash_image = load_image("slash_image.png")

        self.cropRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.slashcropRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.positionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.skillpositionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.slashpositionRect = SDL_Rect(int(0),int(0),int(0),int(0))
        self.gravity = 9.8
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
        self.slashcropRect.w = self.slash_image.w
        self.slashcropRect.h = self.slash_image.h

        self.skillpositionRect.x = self.positionRect.x = X
        self.skillpositionRect.y = self.positionRect.y = Y
        self.skillpositionRect.w = self.skill_image.w
        self.skillpositionRect.h = self.skill_image.h

        self.slashpositionRect.x = X
        self.slashpositionRect.y = Y - 50

        self.cropRect.w = int (self.cropRect.w/5)
        self.cropRect.h = int (self.cropRect.h/5)
        self.slashcropRect.h = int(self.slashcropRect.h/18)

        self.frameWidth = self.positionRect.w = self.cropRect.w
        self.frameHeight = self.positionRect.h = self.cropRect.h

        self.slashpositionRect.w = self.slashcropRect.w
        self.slashpositionRect.h = self.slashcropRect.h

        self.slashframeHeight = self.slashcropRect.h

        self.originX = self.frameWidth / 2
        self.originY = self.frameHeight / 2

        self.isActive = 0
        self.total_frames = 0 ;
        self.slash_frames = 0;

    def handle_event(self, event):

        self.isActive = 1

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            self.ATTACK = True

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            if self.SKILL_value >= 100:
                self.SKILL = True
                self.SKILL_value = 0

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):

            if self.state in (self.BASIC_STATE,):

                if self.Collision==True:
                    self.state = self.BASIC_STATE
                else:
                    self.DAMAGE = True
                    self.moveSpeed = 700
                    self.state = self.JUMP_STATE
                    self.JUMP_UP = True


        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):

            if self.DEFENSE_value >= 80:
                self.DEFENSE = True
                self.DEFENSE_value -= 80

                if self.state in (self.BASIC_STATE,):
                    self.state = self.DEFENSE_STATE
                    self.BASIC_DEFENSE = True

                if self.state in (self.JUMP_STATE,):
                    self.state = self.DEFENSE_STATE
                    self.JUMP_DEFENSE = True


        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
                self.isActive = 0
                self.DEFENSE = False
                if((self.JUMP_DOWN == True) or (self.JUMP_UP == True)):
                        self.state = self.JUMP_STATE
                else:
                        self.state = self.BASIC_STATE
                self.JUMP_DEFENSE = False
                self.BASIC_DEFENSE = False

    def Update(self,delta):

        if self.SKILL == False:
            if ((self.state == self.JUMP_STATE)):
                self.positionRect.y = int(self.positionRect.y - (self.moveSpeed * delta))
                self.moveSpeed = self.moveSpeed - self.gravity

            if self.state in (self.DEFENSE_STATE,):
                if(self.JUMP_DEFENSE == True):
                    self.positionRect.y = int(self.positionRect.y - (self.moveSpeed * delta))
                    self.moveSpeed = self.moveSpeed - self.gravity

            if self.GetOriginY() <= self.TOP:
                        self.JUMP_DOWN =True
                        self.JUMP_UP = False


            if self.GetOriginY() >= self.BOTTOM :
                        self.JUMP_DOWN = False
                        if(self.BASIC_DEFENSE == True):
                            self.state = self.DEFENSE_STATE
                        else:
                            self.state = self.BASIC_STATE

                        self.moveSpeed = 0

            self.cropRect.y = self.frameHeight*self.state

        elif self.SKILL == True:
            if self.GetOriginY() >= 100:
                self.positionRect.y = int(self.positionRect.y - (1000 * delta))

            else:
                self.moveSpeed = 0
                self.positionRect.y = 1270
                self.SKILL = False

        if self.DEFENSE_value < 210:
            self.DEFENSE_value += delta * 20

        if(self.isActive):

                if(self.ATTACK == True):
                    self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * delta
                    self.cropRect.x = (int(self.total_frames) % 5) * self.frameWidth

                    if (self.cropRect.x == 512):
                        self.ATTACK = False
                        self.isActive = 0
                        self.DAMAGE = True

                if (self.DEFENSE == True):
                    if self.state == self.DEFENSE_STATE:
                        self.total_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * delta
                        if(self.total_frames > 4):
                            self.total_frames = 4
                        self.cropRect.x = (int(self.total_frames) % 5) * self.frameWidth

                    else:
                        self.cropRect.x = (0 % 5) * self.frameWidth

                    if(self.DEFENSE_ON == True):

                            self.cropRect.y = (int(4 % 5) * self.frameWidth)
                            self.cropRect.x = (0 % 5) * self.frameWidth

                if (self.HIT == True):
                    self.slash_frames += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * delta
                    self.slashcropRect.y = (int(self.slash_frames) % 18) * self.slashframeHeight

                if (self.slashcropRect.y >= 2176):
                    self.HIT = False
                    self.slash_frames = 0

        else:
            self.cropRect.x = 0
            self.total_frames = 0


        self.skillpositionRect.x = self.positionRect.x
        self.skillpositionRect.y = self.positionRect.y


    def Draw(self,cameraRect):

        if (self.SKILL == False):
            self.image.user_Objects_draw(self.cropRect,self.positionRect,cameraRect)

        elif (self.SKILL == True):
            self.skill_image.dynamic_draw(self.skillpositionRect, cameraRect)

        if (self.HIT == True):
            self.slashpositionRect.y = self.positionRect.y - 50
            self.slash_image.user_Objects_draw(self.slashcropRect, self.slashpositionRect, cameraRect)


    def IntersectsWith(self,Building):

        if(self.collide(Building) and self.SKILL == False):

                SDL_SetTextureColorMod(self.image.texture, 255, 0,0)
                self.Collision = True
                self.moveSpeed = Building.moveSpeed - 10

                if (self.ATTACK == True):
                    Building.HIT = True
                    self.HIT = True
                    self.slash_frames = 0

                if (self.DEFENSE == True):
                    self.DEFENSE_ON = True
                    Building.moveSpeed = 20
                    Building.DEFENSE = True
                    self.moveSpeed = -400

                if (self.state == self.BASIC_STATE and self.DAMAGE == True):
                    self.HP -= 1
                    self.DAMAGE = False
                return True

        elif (self.collide(Building) and self.SKILL == True):
            self.Collision = True
            Building.HP = 0

            return True


        SDL_SetTextureColorMod(self.image.texture, 255, 255, 255)
        self.Collision = False
        Building.HIT = False
        self.DEFENSE_ON = False
        return False

    def collide(self, Building):
        left_a, bottom_a, right_a,top_a = self.get_bb()
        left_b, bottom_b, right_b,top_b = Building.get_bb()

        if (left_a > right_b):
            return False
        if (right_a < left_b):
            return False
        if (top_a < bottom_b):
            return False
        if (bottom_a > top_b):
            return False
        return True

    def get_bb(self):
        return self.GetOriginX() - 30,self.GetOriginY() - 30, self.GetOriginX() + 30, self.GetOriginY() + 30

    def GetOriginX(self):
        return abs((self.positionRect.x + self.originX))

    def GetOriginY(self):
        return abs((self.positionRect.y + self.originY))

    def __del__(self):
        pass
