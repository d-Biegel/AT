#importing
import time
import math
import random
import pygame as pg


#initialize pygame
pg.init()

WIDTH, HEIGHT = 1000, 800

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Accuracy Trainer")

#Initializing variables
TARGET_INCREMENT = 400
TARGET_EVENT = pg.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0, 25, 70)
LIVES = 25
TOP_BAR_HEIGTH = 50

LABEL_FONT = pg.font.SysFont("comicsans", 24)

#Target class
class Target:
    MAX_SIZE = 30
    GROW_RATE = 0.2 #per frame
    TARGET_COLOR = 'red'
    SECOND_COLOR = 'white'

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROW_RATE >= self.MAX_SIZE: #If by next update the target size would have been >= MAX, then it can stop growing
            self.grow = False

        if self.grow:
            self.size += self.GROW_RATE #growing target
        else:
            self.size -= self.GROW_RATE #shrinking target
        
    def draw(self, win):
        pg.draw.circle(win, self.TARGET_COLOR, (self.x, self.y), self.size)
        pg.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)  #Draw multiple circles that overlap eachother to appear as a target
        pg.draw.circle(win, self.TARGET_COLOR, (self.x, self.y), self.size * 0.6)
        pg.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)


    def collide(self, x, y):
        dis = math.sqrt((self.x - x) **2 + (self.y - y) **2) #equation for distance from center of target and mouse click point is within the radius, then we clicked thr target
        return dis <= self.size
        
#Display and timer functions
def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)
        
    
   
#Formating timer function
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs%60,1))
    mins = int(secs // 60)

    return f"{mins:02d}:{seconds:02d}.{milli}"
#Display bar on top of screen
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pg.draw.rect(win, 'grey', (0,0, WIDTH, TOP_BAR_HEIGTH))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1,"black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
    misses_label = LABEL_FONT.render(f"Misses: {misses}", 1, "black")

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200,5))
    win.blit(hits_label, (450,5))
    win.blit(lives_label, (650,5))
    win.blit(misses_label, (850, 5))



def end_sceen(win, elapsed_time, targets_pressed, clicks, misses):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1,"white")
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} targets/sec", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks *100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")
    misses_label = LABEL_FONT.render(f"Misses: {misses}", 1, "white")

    win.blit(time_label, (get_middle(time_label),100))
    win.blit(speed_label, (get_middle(speed_label),200))
    win.blit(hits_label, (get_middle(hits_label),300))
    win.blit(accuracy_label, (get_middle(accuracy_label),400))
    win.blit(misses_label, (get_middle(misses_label), 500))

    pg.display.update()

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2







def main():
    run = True
    targets = []
    clock = pg.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pg.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pg.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGTH, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)
            
                

            if event.type == pg.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
                misses += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_sceen(WIN, elapsed_time, targets_pressed, clicks, misses) #end game
        
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pg.display.update()
    pg.quit()

if __name__ == "__main__":
    main()
