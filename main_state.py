import random
import json
import os

from pico2d import *

from debris import *
from background import Background
from building1 import Building1
from building2 import Building2
from building3 import Building3
from player import Player
from ui import UI

import game_framework
import title_state

name = "MainState"

player = None
background = None
buildings = None
wreckages = None
camerRect = None
ui = None
count = 0
state = 0

def enter():
    global player,background,buildings,camerRect,wreckages,ui,state

    background = Background()
    buildings = []
    wreckages = []
    ui = UI()

    player = Player(320, 1270)
    camerRect = SDL_Rect(int(0),int(0),int(640),int(480))

    game_framework.reset_time()

    state = 0

def exit():
    global player,background,buildings,camerRect,wreckages,ui
    ui.Record_score()
    del(player)
    del(background)
    del(buildings)
    del(camerRect)
    del(wreckages)
    del(ui)

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

    global player,background,buildings,camerRect,wreckages,ui,count,state

    r = random.randint(0,2)

    count += frame_time

    player.Update(frame_time)

    for building in buildings:
        building.Update(frame_time)
        player.IntersectsWith(building)

    for building in buildings:
        if(building.Broken_on == True):
            wreckages.append(Wreckage(int(building.GetOriginX()), int(building.GetOriginY())))
            building.Broken_on = False
            player.SCORE += building.SCORE
            if (player.SKILL_value < 100):
                player.SKILL_value += 10

        if(building.Broken):
            buildings.remove(building)
            if state == 1:
                state = 0
                if player.SKILL == True:
                    player.positionRect.y = 1270
                    player.SKILL = False
            #buildings.append(Building1("building1.png", 130, 100))

    if state == 0:
        if int(count % 8) == 0:
            if r == 0:
                buildings.append(Building1(130, -500))
                count += 1
            if r == 1:
                buildings.append(Building2(180,-500))
                count += 1
            if r == 2:
                buildings.append(Building3(70,-500))
                count += 1

    for Broken in wreckages:
        Broken.Update(frame_time)
        if(Broken.remove):
            wreckages.remove(Broken)

    camerRect.x = abs(int(player.GetOriginX()-320))
    camerRect.y = abs(int(player.GetOriginY()-240))

    if(camerRect.y <0):
            camerRect.y= 0
    if(camerRect.y + camerRect.h>=background.GetHeight()):
            camerRect.y = background.GetHeight() - 480

    ui.Update(player)

    if (player.HP == 0):
        game_framework.change_state(title_state)

def draw(frame_time):

    global player, background, buildings, camerRect, wreckages, ui, state

    clear_canvas()

    if state == 0:
        background.Draw(camerRect)


    for building in buildings:
        building.Draw(camerRect)

    for Broken in wreckages:
        Broken.Draw(camerRect)


    player.Draw(camerRect)
    ui.Draw()

    update_canvas()
