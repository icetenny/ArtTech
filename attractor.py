import pygame
import random
import math
import time

class Attractor:
    def __init__(self):
        self.is_active = False
        self.pos = (0, 0)