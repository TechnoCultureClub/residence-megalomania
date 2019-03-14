import pygame


WIDTH = 320
HEIGHT = 240
FPS = 30

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
buttons = joystick.get_numbuttons()
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


def show_go_screen():
    """ Create the game over screnn """
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.JOYBUTTONUP:
                print(event.button)
            if event.type == pygame.JOYAXISMOTION:
                #print("AXES 3 {} / AXES 4 {}".format(joystick.get_axis(3),joystick.get_axis(4)))
                if event.axis == 3 and event.value > 0.1:
                    print("A droite")
                if event.axis == 3 and event.value < -0.1 :
                    print("A gauche")


show_go_screen()
