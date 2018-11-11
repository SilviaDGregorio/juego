#!/usr/bin/env python3

import pygame
from player import Player
from floor import Floor
from door import Door
from pygame.locals import *


SCREENRECT     = Rect(0, 0, 699, 525)


class Map(object):
    _map = {}

    def __init__(self, width, height):
        super(Map, self).__init__()
        self.width = width
        self.height = height
        for y in range(0, self.height):
            self._map[y] = {}
            for x in range(0, self.width):
                self._map[y][x] = '0'

    def __init__(self, rows):
        super(Map, self).__init__()
        self.height = len(rows)
        self.width = len(rows[0])
        for y, row in enumerate(rows):
            self._map[y] = {}
            for x, item in enumerate(row):
                if item == '#':
                    self._map[y][x] = Floor()
                elif item == '|':
                    self._map[y][x] = Door()
                elif item == '@':
                    self._map[y][x] = Player()
                else:
                    self._map[y][x] = None  
    
    def get(self, x, y):
        return self._map[y][x]

    def load(fname):
        '''
        Creates a squared map from a string separated by \n
        0 => outside of the map
        # => walkable path
        | => door
        @ => player

        '''
        mapstring = ''
        with open(fname) as f:
            mapstring = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        mapstring = [x.strip() for x in mapstring]
        return Map(mapstring)