from object import *

player = None
background = None
building = None


def handle_events():
    global running
    global player
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)

def main():
    global player
    global background
    global building
    global running

    open_canvas()
    background = Background("background.png")
    building = Building("Building.png", 70, 100)
    player = Player("player.png", 280, 1270, 5, 5)
    cameraRect = SDL_Rect(int(0), int(0), int(640), int(480))

    running = True
    currentTime = 0
    prevTime = 0
    delta = 0.0

    while running:

        prevTime = currentTime
        currentTime = SDL_GetTicks()
        delta = (currentTime - prevTime) / 1000.0

        handle_events()

        player.update(delta)

        cameraRect.x = abs(int(player.GetOriginX() - 320))
        cameraRect.y = abs(int(player.GetOriginY()- 240))

        if(cameraRect.x < 0):
            cameraRect.x = 0
        if(cameraRect.y < 0):
            cameraRect.y = 0
        if(cameraRect.x + cameraRect.w >= background.GetWidth()):
            cameraRect.x = background.GetWidth() - 640
        if(cameraRect.y + cameraRect.h >= background.GetHeight()):
            cameraRect.y = background.GetHeight() - 480

        player.intersectsWith(building)

        clear_canvas()

        background.draw(cameraRect)
        building.draw(cameraRect)
        player.draw(cameraRect)

        update_canvas()

        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()