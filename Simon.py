import pygame as pyg
import time, random, math, sys
pyg.init()
input = False
score = 0

# Game window
screenSize = 600
win = pyg.display.set_mode((screenSize, screenSize))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 100, 0)
light_green = (0, 255, 0)
red = (100, 0, 0)
light_red = (255, 0, 0)
yellow = (100, 100, 0)
light_yellow = (255, 255, 0)
blue = (0, 0, 100)
light_blue = (0, 0, 255)

# Initialize button colors
g_button = green
r_button = red
y_button = yellow
b_button = blue
sound1 = pyg.mixer.Sound("sound1.wav")
sound2 = pyg.mixer.Sound("sound2.wav")
sound3 = pyg.mixer.Sound("sound3.wav")
sound4 = pyg.mixer.Sound("sound4.wav")

# Order of pattern
order = []

# Generates text
def create_text(text, name, font_size, text_color, location):
    font = pyg.font.SysFont(name, font_size, bold = True)
    ren = font.render(text, True, text_color)
    win.blit(ren, (screenSize/2 - ren.get_rect().width/2, screenSize/2 - location))

# Draws to screen
def draw():
    pyg.display.set_caption("Simon Says | Score: " + str(score))
    win.fill(0)
    
    # Draws colored buttons
    pyg.draw.rect(win, g_button, (0, 0, screenSize/2, screenSize/2), border_top_left_radius = screenSize//2)
    pyg.draw.rect(win, r_button, (screenSize/2, 0, screenSize/2, screenSize/2), border_top_right_radius = screenSize//2)
    pyg.draw.rect(win, y_button, (0, screenSize/2, screenSize/2, screenSize/2), border_bottom_left_radius = screenSize//2)
    pyg.draw.rect(win, b_button, (screenSize/2, screenSize/2, screenSize/2, screenSize/2), border_bottom_right_radius = screenSize//2)
    
    # Draws circle and lines
    pyg.draw.circle(win, black, (screenSize//2, screenSize//2), screenSize//5)
    pyg.draw.line(win, black, (screenSize/2, 0), (screenSize/2, screenSize), width = screenSize//10 - 1)
    pyg.draw.line(win, black, (0, screenSize/2), (screenSize, screenSize/2), width = screenSize//10 - 1)
    
    # Prints Score
    create_text("Score: " + str(score), "Courier", 24, white, 10)
    
    pyg.display.update()

# Returns distance between two points
def distance(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    x_squared = (x2 - x1) * (x2 - x1)
    y_squared = (y2 - y1) * (y2 - y1)
    dist = math.sqrt(x_squared + y_squared)
    return dist

# Adds element to pattern
def add2pattern():
    global order
    random.seed()
    temp = random.randrange(1, 5)
    order.append(temp)

# Resets button colors
def default_colors():
    global g_button, r_button, y_button, b_button
    g_button = green
    r_button = red
    y_button = yellow
    b_button = blue

# Displays generated pattern
def display_pattern():
    global g_button, r_button, y_button, b_button, input
    #default_colors()
    for i in order:
        default_colors()
        draw()
        pyg.time.delay(300)
        if i == 1:
            g_button = light_green
            r_button = red
            y_button = yellow
            b_button = blue
            sound1.play()
        elif i == 2:
            g_button = green
            r_button = light_red
            y_button = yellow
            b_button = blue
            sound2.play()
        elif i == 3:
            g_button = green
            r_button = red
            y_button = light_yellow
            b_button = blue
            sound3.play()
        elif i == 4:
            g_button = green
            r_button = red
            y_button = yellow
            b_button = light_blue
            sound4.play()
        draw()
        pyg.time.delay(300)
    input = True

def gameloop():
    global g_button, r_button, y_button, b_button, input, score, order
    gameover = False
    run = True
    score = 0
    order = []
    
    while run:
        # GAMEOVER SCREEN
        while gameover:
            win.fill(black)
            for e in pyg.event.get():
                if e.type == pyg.QUIT:
                    run = False
                    gameover = False
                    pyg.quit()
                    sys.exit()
                if e.type == pyg.MOUSEBUTTONUP:
                    gameover = False
                    gameloop()
            create_text("GAME OVER", "Courier", 48, white, 150)
            create_text("Score: " + str(score), "Courier", 36, white, 60)
            create_text("Click anywhere to play again", "Courier", 18, white, -25)
            pyg.display.update()
        
        user_order = []
        count = 0 
        add2pattern()
        display_pattern()
        
        # MOUSE AND BUTTON INTERACTION
        while input:
            for e in pyg.event.get():
                # Clicking X to quit
                if e.type == pyg.QUIT:
                    input = False
                    run = False
                    pyg.quit()
                    sys.exit()
                
                # Outer two if-statements detect if mouse is inside of a button
                # Innermost if-statement executes if mouse is clicked
                
                # Distance between mouse and center of screen
                m_x,m_y = pyg.mouse.get_pos()
                dist = distance((m_x, m_y), (screenSize/2, screenSize/2))
                
                # Green
                if m_x <= screenSize/2 - ((screenSize/10) / 2) and m_y <= screenSize/2 - ((screenSize/10) / 2):
                    if dist > screenSize/5 and dist < screenSize/2:
                        g_button = light_green
                        if e.type == pyg.MOUSEBUTTONUP:
                            user_order.append(1)
                            count += 1
                            sound1.play()
                    else:
                        g_button = green
                else:
                    g_button = green
                    
                # Red
                if m_x >= screenSize/2 + ((screenSize/10) / 2) and m_y <= screenSize/2 - ((screenSize/10) / 2):
                    if dist > screenSize/5 and dist < screenSize/2:
                        r_button = light_red
                        if e.type == pyg.MOUSEBUTTONUP:
                            user_order.append(2)
                            count += 1
                            sound2.play()
                    else:
                        r_button = red
                else:
                    r_button = red
                
                # Yellow
                if m_x <= screenSize/2 - ((screenSize/10) / 2) and m_y >= screenSize/2 + ((screenSize/10) / 2):
                    if dist > screenSize/5 and dist < screenSize/2:
                        y_button = light_yellow
                        if e.type == pyg.MOUSEBUTTONUP:
                            user_order.append(3)
                            count += 1
                            sound3.play()
                    else:
                        y_button = yellow
                else:
                    y_button = yellow
                    
                # Blue
                if m_x >= screenSize/2 + ((screenSize/10) / 2) and m_y >= screenSize/2 + ((screenSize/10) / 2):
                    if dist > screenSize/5 and dist < screenSize/2:
                        b_button = light_blue
                        if e.type == pyg.MOUSEBUTTONUP:
                            user_order.append(4)
                            count += 1
                            sound4.play()
                    else:
                        b_button = blue
                else:
                    b_button = blue
            
            # Checking if player is pressing the correct buttons
            for i in range(count):
                if order[i] == user_order[i]:
                    if len(order) == len(user_order) and i == count - 1:
                        input = False
                        default_colors()
                        draw()
                        score += 1
                        pyg.time.delay(500)
                        break
                else:
                    input = False
                    gameover = True
                    break
            draw()

gameloop()
