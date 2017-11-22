import sys
import types
import ctypes
import math

from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlttf import *

lattice_on = True


def delay(sec):
    SDL_Delay(int(sec*1000))

def get_time():
    return SDL_GetTicks() / 1000.0


def open_canvas(w=640, h=480, sync=False):
    global window, renderer
    global canvas_width, canvas_height
    global debug_font

    canvas_width, canvas_height = w, h
    SDL_Init(SDL_INIT_EVERYTHING)
    IMG_Init(IMG_INIT_JPG | IMG_INIT_PNG | IMG_INIT_TIF | IMG_INIT_WEBP)
    TTF_Init()
    caption = ('Pico2D Canvas (' + str(w) + 'x' + str(h) + ')' + ' 1000.0 FPS').encode('UTF-8')

    window = SDL_CreateWindow(caption, SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, w, h, SDL_WINDOW_SHOWN)

    if sync:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
    else:
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED)
    clear_canvas()
    update_canvas()
    clear_canvas()
    update_canvas()
    debug_font = load_font('CONSOLA.TTF', 20)

def show_lattice():
    global lattice_on
    lattice_on = True
    clear_canvas()
    update_canvas()

def hide_lattice():
    global lattice_on
    lattice_on = False
    clear_canvas()
    update_canvas()

def close_canvas():
    TTF_Quit()
    IMG_Quit()
    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)
    SDL_Quit()

def clear_canvas():
    SDL_SetRenderDrawColor(renderer, 200, 200, 210, 255)
    SDL_RenderClear(renderer)
    if lattice_on:
        SDL_SetRenderDrawColor(renderer, 180, 180, 180, 255)
        for x in range(0, canvas_width, 10):
            SDL_RenderDrawLine(renderer, x, 0, x, canvas_height)
        for y in range(canvas_height-1, 0, -10):
            SDL_RenderDrawLine(renderer, 0, y, canvas_width, y)
        SDL_SetRenderDrawColor(renderer, 160, 160, 160, 255)
        for x in range(0, canvas_width, 100):
            SDL_RenderDrawLine(renderer, x, 0, x, canvas_height)
        for y in range(canvas_height-1, 0, -100):
            SDL_RenderDrawLine(renderer, 0, y, canvas_width, y)

def clear_canvas_now():
	clear_canvas()
	update_canvas()
	clear_canvas()
	update_canvas()

def update_canvas():
    SDL_RenderPresent(renderer)

def show_cursor():
    SDL_ShowCursor(SDL_ENABLE)

def hide_cursor():
    SDL_ShowCursor(SDL_DISABLE)

cur_time = 0.0
def print_fps():
    global window
    global cur_time
    global canvas_width, canvas_height
    dt = get_time() - cur_time
    cur_time += dt
    dt = max(dt, 0.0001)
    caption = ('Pico2D Canvas (' + str(canvas_width) + 'x' + str(canvas_height) + ')' + ' %4.2f FPS' % (1.0/dt)).encode('UTF-8')
    SDL_SetWindowTitle(window, caption)


def debug_print(str):
    global canvas_height
    global debug_font
    debug_font.draw(0, canvas_height - 10, str)

class Event:
    def __init__(self, evt_type):
        self.type = evt_type
        self.key = None
        self.button = None
        self.x = None
        self.y = None


def get_events():
    print_fps()
    SDL_Delay(1)
    sdl_event = SDL_Event()
    events = []
    while SDL_PollEvent(ctypes.byref(sdl_event)):
        event = Event(sdl_event.type)
        if event.type in (SDL_QUIT, SDL_KEYDOWN, SDL_KEYUP, SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            events.append(event)
            if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
                if not sdl_event.key.repeat:
                    event.key = sdl_event.key.keysym.sym
            elif event.type == SDL_MOUSEMOTION:
                event.x, event.y = sdl_event.motion.x, sdl_event.motion.y
            elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
                event.button, event.x, event.y = sdl_event.button.button, sdl_event.button.x, sdl_event.button.y

    return events


def to_sdl_rect(x,y,w,h):
    return SDL_Rect(int(x), int(-y+canvas_height-h), int(w), int(h))

def draw_rectangle(x1,y1,x2,y2):
    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
    rect = SDL_Rect(int(x1),int(-y1+canvas_height),abs(int(x2-x1)),abs(int(y1-y2)))
    SDL_RenderDrawRect(renderer, rect)

class Image:

    def __init__(self, texture):
        self.texture = texture
        # http://wiki.libsdl.org/SDL_QueryTexture
        w, h = c_int(), c_int()
        SDL_QueryTexture(self.texture, None, None, ctypes.byref(w), ctypes.byref(h))
        self.w, self.h = w.value, h.value

    def __del__(self):
        SDL_DestroyTexture(self.texture)

    def rotate_draw(self, rad, x, y, w = None, h = None):
        if w == None and h == None:
            w,h = self.w, self.h
        rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        SDL_RenderCopyEx(renderer, self.texture, None, rect, math.degrees(-rad), None, SDL_FLIP_NONE);

    def draw(self, x, y, w=None, h=None):
        if w == None and h == None:
            w,h = self.w, self.h
        rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        SDL_RenderCopy(renderer, self.texture, None, rect);

    def clip_draw(self, left, bottom, width, height, x, y, w=None, h=None):
        """Clip a rectangle from image and draw"""
        if w == None and h == None:
            w,h = width, height
        src_rect = SDL_Rect(left, self.h - bottom - height, width, height)
        dest_rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        SDL_RenderCopy(renderer, self.texture, src_rect, dest_rect);

    def draw_now(self, x, y, w=None, h=None):
        self.draw(x,y,w,h)
        update_canvas()
        self.draw(x,y,w,h)
        update_canvas()
        '''
        if w == None and h == None:
            w,h = self.w, self.h
        rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        SDL_RenderCopy(renderer, self.texture, None, rect);
        SDL_RenderPresent(renderer)
        '''
    def static_Object_draw(self,cameraRect):
        SDL_RenderCopy(renderer,self.texture,cameraRect,None)

    def dynamic_draw(self,positionRect,cameraRect):
        drawingRect = SDL_Rect((int(positionRect.x) - int(cameraRect.x)), ((int(positionRect.y) - int(cameraRect.y))+canvas_height - cameraRect.h), int(positionRect.w), int(positionRect.h))
        SDL_RenderCopy(renderer,self.texture,None,drawingRect)

        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
        SDL_RenderDrawRect(renderer, drawingRect)

    def dynamic_Object_draw(self,cropRect,positionRect,cameraRect):
        drawingRect = SDL_Rect(abs(int(positionRect.x) - int(cameraRect.x)), ((int(positionRect.y) - int(cameraRect.y))+canvas_height - cameraRect.h), int(positionRect.w), int(positionRect.h))
        SDL_RenderCopy(renderer,self.texture,cropRect,drawingRect)

        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
        SDL_RenderDrawRect(renderer, drawingRect)


    def user_Objects_draw(self,cropRect,positionRect,cameraRect):
        drawingRect = SDL_Rect(abs(int(positionRect.x) - int(cameraRect.x)), abs(int(positionRect.y) - int(cameraRect.y)), int(positionRect.w), int(positionRect.h))
        SDL_RenderCopy(renderer,self.texture,cropRect,drawingRect)

        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255)
        SDL_RenderDrawRect(renderer, drawingRect)


    def opacify(self, o):
        SDL_SetTextureAlphaMod(self.texture, int(o*255.0))

def load_image(name):
    texture = IMG_LoadTexture(renderer, name.encode('UTF-8'));
    if (not texture):
	    print('cannot load %s' % name)
	    raise IOError

    image = Image(texture)
    return image


class Font:
    def __init__(self, name, size=20):
        self.font = TTF_OpenFont(name.encode('utf-8'), size)

    def draw(self, x, y, str, color=(0,0,0)):
        sdl_color = SDL_Color(color[0], color[1], color[2])
        surface = TTF_RenderText_Blended(self.font, str.encode('utf-8'), sdl_color)
        texture = SDL_CreateTextureFromSurface(renderer, surface)
        SDL_FreeSurface(surface)
        image = Image(texture)
        image.draw(x+image.w/2, y)


def load_font(name, size = 20):
    font = Font(name, size)
    return font



def test_pico2d():
    print('testing pico2d')
    print('done')


print("Pico2d is prepared.")
if __name__ == "__main__":
    test_pico2d()


