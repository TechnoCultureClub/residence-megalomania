# Pygame template - skeleton for a new pygame project
import random
import os
import sys
import json
import pygame


# Screen Size
WIDTH = 480
HEIGHT = 320
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK2 = (2, 2, 2)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_PLAYER1 = (42, 42, 42)
BG_PLAYER2 = (42, 42, 42)
BG_PLAYER_CHARLES = (99, 99, 99)


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
#screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
# pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Variables
SIZE = 73  # Emoji Size in the Srpite Sheet
SCALE_SIZE = 40  # Emoji Size diplayed on the screen
SCALE_SIZE_LITTLE = 30  # Size of the player's Avatar displayed on the screen
Level = 10  # Number of Emoji shown on screen
max_countdown = 30000
last_now = 0
width_progressbar = WIDTH
OFFSET_X = 50

# Load Images and Background
screen_player_1_bg = pygame.image.load('data/screen_player_1_bg.png').convert()
screen_player_1_bg_rect = screen_player_1_bg.get_rect()

screen_player_2_bg = pygame.image.load(
    'data/screen_player_2_bg_ok.png').convert()
screen_player_2_bg_rect = screen_player_2_bg.get_rect()

screen_go_bg = pygame.image.load('data/screen_go_bg_dark.png').convert()
pygame.transform.scale(screen_go_bg, (WIDTH, HEIGHT))
screen_go_bg_rect = screen_go_bg.get_rect()

bg_player_instruction = pygame.image.load(
    'data/bg_player_instruction_dark.png').convert()
pygame.transform.scale(bg_player_instruction, (WIDTH, HEIGHT))
bg_player_instruction_rect = bg_player_instruction.get_rect()

locker_img = pygame.image.load('data/locker_img.png').convert()
locker_img.set_colorkey(BLACK2)
locker_img_rect = locker_img.get_rect()

carre_img = pygame.image.load('data/carrerougeVide.png').convert()
carre_img.set_colorkey(WHITE)
carre_img_rect = carre_img.get_rect()

# Decompte
decompte_list = []
# script_dir = os.path.dirname(__file__)
# decompte_path = os.path.join(script_dir, 'data/Decompte/')
for i in range(30):
    path = ''.join(['data/Decompte/', str(i+1), '.png'])
    decompte_list.append(pygame.transform.scale(pygame.image.load(path).convert(),(SCALE_SIZE+10,SCALE_SIZE+10)))


# Prepare inline Display
inlineRects = []
for i in range(Level):
    inlineRects.append(pygame.Rect(OFFSET_X+(i*SCALE_SIZE),
                                   SCALE_SIZE*2.3, SCALE_SIZE, SCALE_SIZE))

#two_lines_rect = []
#for i in range(2):
#    two_lines_rect.append([])
#    for j in range(int(Level/2)):
#        two_lines_rect[i].append(pygame.Rect(
#            (j*SCALE_SIZE), SCALE_SIZE*2, SCALE_SIZE, SCALE_SIZE))

inlineRects2 = []
for i in range(Level):
    inlineRects2.append(pygame.Rect(OFFSET_X+(i*SCALE_SIZE),
                                    SCALE_SIZE*3, SCALE_SIZE_LITTLE, SCALE_SIZE_LITTLE))

inlineRects3 = []
for i in range(Level):
    inlineRects3.append(pygame.Rect(70+(i*(SCALE_SIZE+20)),
                                    220, SCALE_SIZE_LITTLE, SCALE_SIZE_LITTLE))


# Init JoyStick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define Path
#script_dir = os.path.dirname(__file__)
#data_path = os.path.join(script_dir, 'data/phrases.json')

# Open the JSON data file


def peakDataFromFile(path):
    """ According to a random number we select a question in the JSON file """
    line = random.randint(1, 15)
    f = open(path)
    data = json.load(f)
    data = data['Enigmes'][line]
    return data

# Creae Surface of emoji


def createEmojiSurface(data):
    """ Function to create the list of surfaces used to handle each emoji """
    sheet = pygame.image.load('data/sprites.png').convert()

    # Retrieve x,y coordinates from data and set Up rectangles for each Emoji
    Rects = []
    for i in range(0, Level*2, 2):
        x = ((int(data['coordonnees'][i])-1)*SIZE)
        y = ((int(data['coordonnees'][i+1])-1)*SIZE)
        Rects.append(pygame.Rect(x, y, SIZE, SIZE))

    # Create a list of subSurface for each selected Emoji
    emoji = []
    for i in range(Level):
        emoji.append(sheet.subsurface(Rects[i]))

    return emoji


font_name = pygame.font.match_font('Consolas')


def drawText(surf, text, size, x, y, center=None, color=None):
    """ Function that handle text printing """
    font = pygame.font.Font(font_name, size)
    if color is not None:
        text_surface = font.render(text, True, color)
    else:
        text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    if center == 'center':
        text_rect.midtop = (WIDTH/2, y)
    else:
        text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)


def showGoScreen():
    """ Create the game over screnn """
    screen.blit(screen_go_bg, screen_go_bg_rect)
    # drawText(screen, 'MEGALOMANIA', 30, WIDTH/2, HEIGHT/4, 'center')
    drawText(screen, 'POUR COMMENCER APPUYER SUR START',
             18, 150, 120, 'center', WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.JOYBUTTONUP:
                waiting = False


def showNewRoundScreen(reponse):
    """ New Round screen """
    global game_over, new_round, screen_player_1, screen_player_2, new_game

    screen.blit(bg_player_instruction, bg_player_instruction_rect)
    if (player_2.get_locker_number() == 0 or player_2.get_locker_number() >= 5):
        drawText(screen, 'FIN DE LA PARTIE !', 20, WIDTH/2, HEIGHT/8, 'center')
        new_game = True
        game_over = True
        new_round = False
        screen_player_1 = True
        screen_player_2 = False
    else:
        if reponse:
            drawText(screen, 'BRAVO ! Cadenas restants:',
                     20, WIDTH/2, HEIGHT/8, 'center')
        else:
            drawText(screen, "Non, ce n'est pas ça ! Cadenas restants: ",
                     20, WIDTH/2, HEIGHT/8, 'center')
        #drawText(screen, 'Cadenats restants avant liberation:', 18, 0, HEIGHT/4, 'notcenter')
        game_over = False
        new_round = False
        screen_player_1 = True
        drawText(screen, str(player_2.get_locker_number()), 25, WIDTH/2, HEIGHT/4, 'center')
    # all_sprites_lockers.draw(screen)
    drawText(screen, 'POUR CONTINUER PRESSER START ', 20, WIDTH/2, HEIGHT-20, 'center', WHITE)
    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.JOYBUTTONUP:
                waiting = False


def initPlayer2Screen(question):
    """Init is just moving the Surface for the screen 2"""
    for i in range(len(question)):
        question.sprites()[i].rect.y = inlineRects[i].y-45
        question.sprites()[i].rect.x = inlineRects[i].x+90


class Emoji(pygame.sprite.Sprite):
    """ Class for a single Emoji Sprites"""

    def __init__(self, images=None, position=None, scale=None):
        pygame.sprite.Sprite.__init__(self)
        if images and position is not None:
            if scale is not None:
                self.image = pygame.transform.scale(images, (scale, scale))
                self.image.set_colorkey(WHITE)
            else:
                self.image = pygame.transform.scale(
                    images, (SCALE_SIZE, SCALE_SIZE))
                self.image.set_colorkey(BLACK)
            self.rect = images.get_rect()
            self.rect.x = position.x
            self.rect.y = position.y

    def move_to(self, indice):
        """ Function to move the surface by steps of indices """
        self.rect.x = indice*SCALE_SIZE+OFFSET_X+50
        self.rect.y = SCALE_SIZE*5.1

    def moveToRect(self, rect):
        """ Function to move the surface by Rect coordinates """
        self.rect = rect


class Cursor(pygame.sprite.Sprite):
    """ Class that handle the cursor """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = carre_img
        # self.image = pygame.Surface((SCALE_SIZE, 2))
        self.image.set_colorkey(WHITE)
        # pygame.transform.scale(self.image, (SCALE_SIZE_LITTLE+10, SCALE_SIZE_LITTLE+10))

        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = OFFSET_X
        self.rect.y = 2.27*SCALE_SIZE
        self.speedx = 0
        self.position = 0  # The new position of the cursor
        self.select = 0  # Increment each time we select or unselect a new emoji
        self.emoji = []  # The list of Emoji selected by player 1
        self.selection = pygame.sprite.Group()

    def increment(self):
        """ increment """
        self.speedx = 0
        self.position += 1
        self.speedx = +SCALE_SIZE
        self.rect.x += self.speedx
        if self.position > Level-1:
            self.position = Level-1
            self.rect.right = OFFSET_X+Level*SCALE_SIZE

    def decrement(self):
        """ decrement """
        self.speedx = 0
        self.position -= 1
        self.speedx = -SCALE_SIZE
        self.rect.x += self.speedx
        if self.position < 0:
            self.position = 0
            self.rect.left = OFFSET_X

    def add_to_selection(self):
        """Save Selected Emoji to a new sprite Group """
        if self.select <= Level-1:

            self.emoji.append(
                Emoji(emojiSurfaces[self.position], inlineRects2[self.position]))
            self.emoji[self.select].move_to(self.select)

            # Add the selected emoji to the global group stripes to be displayed
            all_sprites_screen_player_1.add(self.emoji[self.select])
            # Also Add it to a separate group to be used later (after screen_player_1 is empty).
            self.selection.add(self.emoji[self.select])
            self.select += 1
            #self.select = Level

    def delete_from_selection(self):
        """ We remove the selected Emoji from the Sprite Group and the list """
        if self.select > 0:
            self.select -= 1
            all_sprites_screen_player_1.remove(self.emoji[self.select])
            self.selection.remove(self.emoji[self.select])
            del self.emoji[self.select]

    def validate_selection(self):
        """ Return the group of emoji selected by player1 """
        return self.selection


class Player(pygame.sprite.Sprite):
    """ Classe Player """

    def __init__(self, avatar_path, locker_number, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(avatar_path).convert()
        self.image.set_colorkey(BLACK)
        pygame.transform.scale(
            self.image, (SCALE_SIZE_LITTLE, SCALE_SIZE_LITTLE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.locker_number = locker_number

    def removeLocker(self):
        self.locker_number -= 1
        all_sprites_lockers.empty()

        for i in range(self.locker_number):
            all_sprites_lockers.add(
                Emoji(locker_img, inlineRects3[i], SCALE_SIZE))
        all_sprites_lockers.add(Emoji(carre_img, inlineRects3[0], SCALE_SIZE+2))


    def addLocker(self):
        self.locker_number += 1
        all_sprites_lockers.empty()

        for i in range(self.locker_number):
            all_sprites_lockers.add(
                Emoji(locker_img, inlineRects3[i], SCALE_SIZE))
        all_sprites_lockers.add(Emoji(carre_img, inlineRects3[0], SCALE_SIZE+2))
    def get_locker_number(self):
        return self.locker_number


class ProgressBar(pygame.sprite.Sprite):
    """ Classe for the timer counter """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = decompte_list[29]
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH,0)
        #self.rect.y = 100
        self.image.set_colorkey(BLACK)
        # self.image = pygame.Surface((width_progressbar, 10))
        # self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        # self.rect = self.image.get_rect()
        # self.rect.x = 0
        # self.rect.y = HEIGHT-100
        # self.width = self.rect.width
        self.i = 30

    def update(self):
        """ Update size of progress bar accorgind to timer """
        
        self.i -= 1
        # self.width -= width_progressbar/(max_countdown/1000)
        # self.image = pygame.Surface((self.width, 10))
        # self.rect = self.image.get_rect()
        # self.rect.x = 0
        # self.rect.y = HEIGHT-100
        self.image = decompte_list[self.i]
        self.image.set_colorkey(BLACK)


########################################
def init():
    """ Init ALl grlibal variables """
    global data, all_sprites_screen_player_1, emojiSurfaces, cursor, all_sprites_screen_player_2
    global countdown, player_1, player_2, all_sprites_lockers

    if new_game:
        # Create a group for each screen
        all_sprites_screen_player_1 = pygame.sprite.Group()
        all_sprites_screen_player_2 = pygame.sprite.Group()
        all_sprites_lockers = pygame.sprite.Group()
        

        # Init Player
        player_1 = Player('data/avatar_player_1.png', 0, WIDTH-50, HEIGHT/2)
        # all_sprites_screen_player_1.add(player_1)
        player_2 = Player('data/avatar_player_2.png', 3, WIDTH-50, HEIGHT/2)
        # all_sprites_screen_player_2.add(player_2)
        # Init Locker Image
        #all_sprites_lockers.empty()
        #all_sprites_lockers.add(Emoji(carre_img, inlineRects3[0], SCALE_SIZE+2))
        for i in range(3):
            all_sprites_lockers.add(Emoji(locker_img, inlineRects3[i], SCALE_SIZE))
        
        all_sprites_lockers.add(Emoji(carre_img, inlineRects3[0], SCALE_SIZE+2))

    # Contdown max value in s
    countdown = 30

    # Create a cursor
    cursor = Cursor()
    all_sprites_screen_player_1.add(cursor)

    # Get a new set of data from Json file
    data = peakDataFromFile('./data/phrases2.json')

    # Peek some emojis according to JSON FILE
    emojiSurfaces = createEmojiSurface(data)

    # Create an instance for each Emoji to display
    for i in range(Level):
        emoji = Emoji(emojiSurfaces[i], inlineRects[i])
        all_sprites_screen_player_1.add(emoji)


# Game loop
global screen_player_1, game_over, new_round, screen_player_2, new_game
new_game = False
running = True
game_over = True
screen_player_1 = True
screen_player_2 = False
screen_introduction = True
screen_player_2_instruction = False
new_round = False
new_game = True
time_is_up = False
reponse = False
while running:

    if game_over:
        showGoScreen()
        game_over = False
        init()

    if new_round:
        showNewRoundScreen(reponse)
        init()
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window

        if event.type == pygame.QUIT:
            running = False

        if screen_player_1:
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0 and event.value > 0.1:
                    cursor.increment()
                elif event.axis == 0 and event.value < -0.1:
                    cursor.decrement()
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 2:
                    cursor.add_to_selection()
                elif event.button == 3:
                    cursor.delete_from_selection()
                elif event.button == 9:
                    # Next screen. Player 2 to play
                    question = cursor.validate_selection()
                    screen_player_1 = False
                    screen_player_2_instruction = True
                    all_sprites_screen_player_1.empty()
        elif screen_player_2_instruction:
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 9:
                    screen_player_2 = True
                    screen_player_2_instruction = False
                    initPlayer2Screen(question)
                    countdown_bar = ProgressBar()
                    all_sprites_screen_player_2.add(countdown_bar)
                    all_sprites_screen_player_2.add(question)
        elif screen_player_2:
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 2 and not time_is_up:  # Good answear
                    all_sprites_screen_player_2.empty()  # Delete  Player 2 Screen

                    # Update Lockers
                    player_2.removeLocker()
                    screen_player_1 = False
                    screen_player_2 = False
                    new_game = False
                    new_round = True
                    reponse = True
                if event.button == 3 and not time_is_up:  # Wrong answear
                    all_sprites_screen_player_2.empty()  # Delete  Player 2 Screen
                    # Update Lockers
                    player_2.addLocker()
                    screen_player_1 = False
                    screen_player_2 = False
                    new_game = False
                    new_round = True
                    reponse = False

        #if event.type == pygame.JOYBUTTONDOWN:
         #   if (event.button == 8 and event.button == 4 and event.button == 5):
          #      all_sprites_screen_player_1.empty()
           #     all_sprites_screen_player_2.empty()
            #    new_game = True
             #   game_over = True
              #  new_round = False
               # screen_player_1 = True
                #screen_player_2 = False    
                #init()


    # Display different Screen
    if screen_player_1:
        # Update
        #all_sprites_screen_player_1.update()

        # Draw / render
        screen.blit(screen_player_1_bg, screen_player_1_bg_rect)
        all_sprites_screen_player_1.draw(screen)
        drawText(screen, 'ENCRYPTE CET ÉNONCÉ', 20, 0, 25, 'center')
        drawText(screen, data['Réponse'], 20, 0, 50, 'center')
        # drawText(screen, "Sélèction: ", 20, 0, SCALE_SIZE*4, 'center')
        drawText(screen, "Sélectionner->'B'/Corriger->'Y'/Valider->'START'",
                 18, 0, HEIGHT-20, 'nocenter', WHITE)

    if screen_player_2_instruction:
        screen.fill(BLACK)
        screen.blit(bg_player_instruction, bg_player_instruction_rect)
        drawText(screen, 'INSTRUCTION:', 20, 0, 0, 'center')

        drawText(screen, "Tourne maintenant l'écran vers ton binôme. ", 18, 0, 50)
        drawText(screen, "Sa mission est de décrypter la série d' émojis", 18, 0, 80)
        drawText(screen, "Mais attention, le temps est limité!", 18, 0, 110)
        drawText(screen, "Si dans les 30 secondes la bonne réponse n'est pas donnée ", 18, 0, 140)   
        drawText(screen, "un nouveau cadenas sera ajouté à la prison  ", 18, 0, 170)
        drawText(screen, "Si il devine correctoment presse 'B' sinon, presse 'Y' ", 18, 0, 200)
        drawText(screen, "Quand vous serez prêt presse 'START' ",20, 0, 250, 'center', WHITE)

    if screen_player_2:
        # screen.fill(BLACK)
        screen.blit(screen_player_2_bg, screen_player_2_bg_rect)
        all_sprites_lockers.draw(screen)
        drawText(screen, 'INDICE:', 20, 0, 135, 'center')
        drawText(screen, data['Question'], 20, 100, 155, 'center')
        drawText(screen, "Si c'est correct presse B sinon, sinon presse Y",
                 18, 0, HEIGHT-20, 'notcentered', WHITE)
        #all_sprites_lockers.draw(screen)
        all_sprites_screen_player_2.draw(screen)
        waiting = True
        now = pygame.time.get_ticks()
        if countdown > 0:
            if now - last_now > 1000:
                all_sprites_screen_player_2.update()
                # all_sprites_screen_player_2.draw(screen)

                last_now = now
                countdown -= 1
                time_is_up = False
        else:
            time_is_up = True
            player_2.addLocker()
            screen.fill(BLACK)
            all_sprites_screen_player_2.empty()
            screen_player_1 = False
            screen_player_2 = False
            new_round = True
            reponse = False

    # *after* drawing everything, flip the display
    pygame.display.flip()
    pygame.event.pump()
pygame.quit()
