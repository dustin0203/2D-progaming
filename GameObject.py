from pico2d import *

class Background():
    def __init__(self, name):
        self.name = name
        self.image = load_image(name)

    def draw(self, cameraRect):
        self.image.static_Object_draw(cameraRect)

    def GetWidth(self):
        return self.image.w

    def GetHeight(self):
        return self.image.h


class Building():
    image = None

    def __init__(self, name, X, Y):
        self.name = name
        if Building.image == None:
            Building.image = load_image(name)

        self.positionRect = SDL_Rect(int(0), int(0), int(0), int(0))
        self.originX = self.image.w / 2
        self.originY = self.image.h / 2
        self.positionRect.x = X
        self.positionRect.y = Y
        self.positionRect.w = self.image.w
        self.positionRect.h = self.image.h
        self.rad = 190

    def draw(self, cameraRect):
        self.image.dynamic_Object_draw(self.positionRect, cameraRect)

    def GetOriginX(self):
        return abs((self.positionRect.x + self.originX))

    def GetOriginY(self):
        return abs((self.positionRect.y + self.originY))

    def GetRad(self):
        return self.rad


class Player():
    BASIC, BASIC_ATTACK, JUMP_ATTACK, DEFENSE, ATTACKER = 0, 0, 2, 4, 3
    JUMP_ON = 1
    JUMP_UP = False
    JUMP_DOWN = False
    TOP = 587
    BOTTOM = 1335

    def __init__(self, name, X, Y, frameX, frameY):
        self.name = name
        self.image = load_image(name)
        self.cropRect = SDL_Rect(int(0), int(0), int(0), int(0))
        self.positionRect = SDL_Rect(int(0), int(0), int(0), int(0))
        self.moveSpeed = 0
        self.frameCounter = 0
        self.frameWidth = 0
        self.frameHeight = 0
        self.textureWidth = 0
        self.isActive = 0
        self.originX = 0
        self.originY = 0
        self.rad = 0
        self.state = self.BASIC
        self.cropRect.w = self.image.w
        self.cropRect.h = self.image.h
        self.gravity = 9.8 / 40
        self.positionRect.x = X
        self.positionRect.y = Y

        self.textureWidth = self.cropRect.w

        self.cropRect.w = int(self.cropRect.w/frameX)
        self.cropRect.h = int(self.cropRect.h/frameY)

        self.frameWidth = self.positionRect.w = self.cropRect.w
        self.frameHeight = self.positionRect.h = self.cropRect.h

        self.originX = self.frameWidth / 2
        self.originY = self.frameHeight / 2

        self.rad = 5
        self.isActive = 0
        self.moveSpeed = 200.0


    def handle_event(self, event):

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if self.state in (self.BASIC, self.JUMP_ON):
                self.isActive = 1
                self.state = self.BASIC_ATTACK

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z):
            if self.state in (self.BASIC_ATTACK, ):
                self.isActive = 0
                self.state = self.BASIC

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            if self.state in (self.BASIC, ):
                self.isActive = 1
                self.state = self.JUMP_ON
                self.JUMP_UP = True

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            if  self.state in (self.BASIC, ):
                self.isActive = 1
                self.state = self.DEFENSE

        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            if self.state in (self.DEFENSE, ):
                self.isActive = 0
                self.state = self.BASIC



    def update(self, delta):

        if (self.state, self.JUMP_UP) == (self.JUMP_ON, True):
            self.positionRect.y = int(self.positionRect.y - (self.moveSpeed * delta))
            self.moveSpeed = self.moveSpeed - self.gravity

        if (self.state, self.JUMP_DOWN) == (self.JUMP_ON, True):
            self.positionRect.y = int(self.positionRect.y + (self.moveSpeed * delta))
            self.moveSpeed = self.moveSpeed + self.gravity

        if self.GetOriginY() <= self.TOP:
            self.JUMP_DOWN = True
            self.JUMP_UP = False
            self.moveSpeed = 200

        if self.GetOriginY() >= self.BOTTOM:
            self.JUMP_DOWN = False
            self.state = self.BASIC
            self.isActive = 0
            self.moveSpeed = 200

        self.cropRect.y = self.frameHeight * self.state


        if(self.isActive):
            self.frameCounter += delta

            if(self.frameCounter >= 0.25):
                self.frameCounter = 0
                self.cropRect.x += self.frameWidth
                if(self.cropRect.x >= self.textureWidth):
                    self.cropRect.x = 0

        else:
            self.frameCounter = 0
            self.cropRect.x = self.frameWidth


    def draw(self, cameraRect):
        self.image.user_Objects_draw(self.cropRect, self.positionRect, cameraRect)


    def intersectsWith(self, Building):
        if(math.sqrt(pow(self.GetOriginX() - Building.GetOriginX(), 2) + pow(self.GetOriginY() - Building.GetOriginY(), 2))
               >= self.rad + Building.GetRad()):
            SDL_SetTextureColorMod(self.image.texture, 255, 255, 255)
            return False

        self.JUMP_DOWN = True
        self.JUMP_UP = False
        SDL_SetTextureColorMod(self.image.texture, 0 , 255, 0)
        return True

    def GetOriginX(self):
        return abs((self.positionRect.x + self.originX))

    def GetOriginY(self):
        return abs((self.positionRect.y + self.originY))

    def GetRad(self):
        return self.rad

    def __del__(self):
        SDL_DestroyTexture(self.texture)








