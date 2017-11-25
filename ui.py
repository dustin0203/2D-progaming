from pico2d import *
from math import *
import random
import json
import os

class UI():
    HP_bar = None
    Index_box = None
    Skill_bar = None
    Defense_bar = None
    Player_index = None
    Score_list = []

    def __init__(self):
        if UI.HP_bar == None:
            UI.HP_bar = load_image("life.png")

        if UI.Index_box == None:
            UI.Index_box = load_image("index_box.png")

        if UI.Skill_bar == None:
            UI.Skill_bar = load_image("skill_bar.png")

        if UI.Defense_bar == None:
            UI.Defense_bar = load_image("defense_bar.png")

        self.font = load_font('FONT.TTF', 70)

    def Update(self, player):
        self.Player_index = player

    def Draw(self):

        self.Index_box.draw(80, 25)

        self.Defense_bar.clip_draw(0,0,int(self.Player_index.DEFENSE_value),16,50,17)

        self.Skill_bar.clip_draw(0,0,self.Player_index.SKILL_value,4,65,33)

        for i in range(0,self.Player_index.HP):
            self.HP_bar.clip_draw(0,0,48,48,200+i*50,25)

        for i in range(0,abs(self.Player_index.HP-3)):
            if i >= 2:
                i = 2
            self.HP_bar.clip_draw(48,0,48,48,300-i*50,25)

        self.font.draw(520,25,'%d' % (self.Player_index.SCORE), (255,0,0))


    def Record_score(self):

        with open('score.txt', 'r') as f:
            self.Score_list = json.load(f)

            # add new score
            self.Score_list.append(self.Player_index.SCORE)

            # write all the scores
            with open('score.txt', 'w') as f:
                json.dump(self.Score_list, f)

        def __del__(self):
            del self.Player_index
            del self.Score_list
