#!/usr/bin/env python3

import random, os.path

#import basic pygame modules
import pygame
from player import Player
from map import Map
from floor import Floor
from door import Door
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


#game constants
MAX_SHOTS      = 2      #most player bullets onscreen
ALIEN_ODDS     = 22     #chances a new alien appears
BOMB_ODDS      = 60    #chances a new bomb will drop
ALIEN_RELOAD   = 12     #frames between new aliens
SCREENRECT     = Rect(0, 0, 699, 525)
SCORE          = 0

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


class dummysound:
    def play(self): pass



class App(object):
    def __init__(self):
        super(App, self).__init__()

    def draw_map(self, map, screen):
                #create the background, tile the bgd image
                bgdtile = load_image('bg.png')
                doortile = load_image('door.png')
                background = pygame.Surface(SCREENRECT.size)

                for y in range(0, map.height):
                    for x in range(0, map.width):
                        if type(map.get(x, y)) is Door:
                            background.blit(doortile, (x * bgdtile.get_width(), y * bgdtile.get_height()))
                        elif type(map.get(x, y)) is Floor :
                            background.blit(bgdtile, (x * bgdtile.get_width(), y * bgdtile.get_height()))
                        elif type(map.get(x, y)) is Player:                            
                            background.blit(bgdtile, (x * bgdtile.get_width(), y * bgdtile.get_height()))

                screen.blit(background, (0, 0))
                pygame.display.flip()
                return background

    

    def main(self, winstyle=0):
        # Initialize pygame
        pygame.init()
       # if pygame.mixer and not pygame.mixer.get_init():
        #    print ('Warning, no sound')
         #   pygame.mixer = None

        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
        screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

        #Load images, assign to sprite classes
        #(do this before the classes are used, after screen setup)
        img = load_image('player1.gif')
        Player.images = [img, pygame.transform.flip(img, 1, 0)]
        
      

        #decorate the game window

        pygame.display.set_caption('Pygame Aliens')
        pygame.mouse.set_visible(0)
        # Initialize Game Groups        
        all = pygame.sprite.RenderUpdates()
        
        #assign default groups to each sprite class
        Player.containers = all 

        main_map = Map.load("map.txt")
        background = self.draw_map(main_map, screen)

        #load the sound effects
        #boom_sound = load_sound('boom.wav')
        #shoot_sound = load_sound('car_door.wav')
       

      

        #Create Some Starting Values
        clock = pygame.time.Clock()

        #initialize our starting sprites
       
        player = Player()
        # Alien() #note, this 'lives' because it goes into a sprite group

        while player.alive():

            #get input
            for event in pygame.event.get():
                if event.type == QUIT or \
                   (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
            keystate = pygame.key.get_pressed()

            # clear/erase the last drawn sprites
            all.clear(screen, background)

            #update all the sprites
            all.update()

            #handle player input
            direction_x = keystate[K_RIGHT] - keystate[K_LEFT]
            direction_y = keystate[K_DOWN] - keystate[K_UP]

            player.move(direction_x, direction_y)
            firing = keystate[K_SPACE]            
            player.reloading = firing
           

            #draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)

            #cap the framerate
            clock.tick(40)

      
        pygame.time.wait(1000)
        pygame.quit()


#call the "main" function if running this script
if __name__ == '__main__':
    App().main()


# def load_sound(file):
#     if not pygame.mixer: return dummysound()
#     file = os.path.join(main_dir, 'data', file)
#     try:
#         sound = pygame.mixer.Sound(file)
#         return sound
#     except pygame.error:
#         print ('Warning, unable to load, %s' % file)
#     return dummysound()



# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard




# class Alien(pygame.sprite.Sprite):
#     speed = 13
#     animcycle = 12
#     images = []
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self, self.containers)
#         self.image = self.images[0]
#         self.rect = self.image.get_rect()
#         self.facing = random.choice((-1,1)) * Alien.speed
#         self.frame = 0
#         if self.facing < 0:
#             self.rect.right = SCREENRECT.right

#     def update(self):
#         self.rect.move_ip(self.facing, 0)
#         if not SCREENRECT.contains(self.rect):
#             self.facing = -self.facing;
#             self.rect.top = self.rect.bottom + 1
#             self.rect = self.rect.clamp(SCREENRECT)
#         self.frame = self.frame + 1
#         self.image = self.images[self.frame//self.animcycle%3]


# class Explosion(pygame.sprite.Sprite):
#     defaultlife = 12
#     animcycle = 3
#     images = []
#     def __init__(self, actor):
#         pygame.sprite.Sprite.__init__(self, self.containers)
#         self.image = self.images[0]
#         self.rect = self.image.get_rect(center=actor.rect.center)
#         self.life = self.defaultlife

#     def update(self):
#         self.life = self.life - 1
#         self.image = self.images[self.life//self.animcycle%2]
#         if self.life <= 0: self.kill()


# class Shot(pygame.sprite.Sprite):
#     speed = -11
#     images = []
#     def __init__(self, pos):
#         pygame.sprite.Sprite.__init__(self, self.containers)
#         self.image = self.images[0]
#         self.rect = self.image.get_rect(midbottom=pos)

#     def update(self):
#         self.rect.move_ip(0, self.speed)
#         if self.rect.top <= 0:
#             self.kill()


# class Bomb(pygame.sprite.Sprite):
#     speed = 9
#     images = []
#     def __init__(self, alien):
#         pygame.sprite.Sprite.__init__(self, self.containers)
#         self.image = self.images[0]
#         self.rect = self.image.get_rect(midbottom=
#                     alien.rect.move(0,5).midbottom)

#     def update(self):
#         self.rect.move_ip(0, self.speed)
#         if self.rect.bottom >= 470:
#             Explosion(self)
#             self.kill()


# class Score(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.font = pygame.font.Font(None, 20)
#         self.font.set_italic(1)
#         self.color = Color('white')
#         self.lastscore = -1
#         self.update()
#         self.rect = self.image.get_rect().move(10, 450)

#     def update(self):
#         if SCORE != self.lastscore:
#             self.lastscore = SCORE
#             msg = "Score: %d" % SCORE
#             self.image = self.font.render(msg, 0, self.color)

