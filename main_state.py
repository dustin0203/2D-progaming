import random
import json
import os

from pico2d import *
from GameObject import *

import game_framework
import title_state


name = "MainState"

player = None
background = None
buildings = None
Brokenbuildings = None

camerRect = None

def enter():
    global player, background, buildings,camerRect,Brokenbuildings
    background = Background("background.png")
    buildings = [Building("building.png",130,200) for i in range(1)]
    Brokenbuildings = []

    player = Player("player.png", 320, 1270, 5, 5)
    camerRect = SDL_Rect(int(0),int(0),int(640),int(480))

    game_framework.reset_time()


def exit():
    global player, background,buildings,camerRect,Brokenbuildings
    del(player)
    del(background)
    del(buildings)
    del(camerRect)
    del(Brokenbuildings)
def pause():
    pass


def resume():
    pass

def handle_events(frame_time):
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        else:

            player.handle_event(event)


def update(frame_time):
    global player, background, buildings,camerRect,Brokenbuildings


    player.Update(frame_time)

    for building in buildings:
        building.Update(frame_time)
        player.IntersectsWith(building)

    for building in buildings:
        if(building.HIT):
             Brokenbuildings.append(Brokenbuilding(int(building.GetOriginX()),int(building.GetOriginY())))
        if(building.Broken):
            buildings.remove(building)
            buildings.append(Building("building.png",130,100))



    for Broken in Brokenbuildings:
        Broken.Update(frame_time)
        if(Broken.remove):
            Brokenbuildings.remove(Broken)


    camerRect.x = abs(int(player.GetOriginX()-320))
    camerRect.y = abs(int(player.GetOriginY()-240))


    if(camerRect.y <0):
            camerRect.y= 0
    if(camerRect.y + camerRect.h>=background.GetHeight()):
            camerRect.y = background.GetHeight() - 480



def draw(frame_time):
    global player, background, buildings,camerRect,Brokenbuildings

    clear_canvas()


    background.Draw(camerRect)

    for building in buildings:
        building.Draw(camerRect)

    for Broken in Brokenbuildings:
        Broken.Draw(camerRect)

    player.Draw(camerRect)

    update_canvas()


