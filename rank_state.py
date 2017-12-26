import game_framework
from pico2d import *
import json
import os

import title_state


name = "Rankstate"
image = None

def enter():
    global image,font
    font = load_font('FONT.TTF',40)
    image = load_image('rankboard.png')

def exit():
    global image,font
    del(image)
    del(font)


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)


def update(frame_time):
    pass


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(400, 300)



    with open('score.txt','r') as f:
        score_list = json.load(f)

    score_list.sort(reverse=True)
    top10= score_list[:10]


    i=0
    for score in top10:
        font.draw(100,450-i*45, ' #[%2d]  S C O R E : %d' % (i+1,score),(255,0,0))
        i+=1

    update_canvas()
