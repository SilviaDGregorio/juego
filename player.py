#!/usr/bin/env python3

#import basic pygame modules
import pygame
from pygame.locals import *


SCREENRECT     = Rect(0, 0, 699, 525)


class Player(pygame.sprite.Sprite):
    speed = 10
    bounce = 24
    gun_offset = -11
    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect =  Rect(100,0, self.image.get_width(), self.image.get_height())
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction_x, direction_y):
        # if direction: self.facing = direction
        self.rect.move_ip(direction_x*self.speed, direction_y*self.speed)
        self.rect = self.rect.clamp(SCREENRECT)
        # if direction < 0:
        #     self.image = self.images[0]
        # elif direction > 0:
        #     self.image = self.images[1]
        # self.rect.top = self.origtop - (self.rect.left//self.bounce%2)

    def gunpos(self):
        pos = self.facing*self.gun_offset + self.rect.centerx
        return pos, self.rect.top
