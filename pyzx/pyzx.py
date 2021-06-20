from decimal import Decimal
from typing import List, Union
from random import random

from pygame import Rect, Surface
import pygame.transform

from pyzx.utils import get_closest

Numeric = Union[Decimal, int, float]
GenericPoint2D = tuple[Numeric, Numeric]


class Point2D:
    def __init__(self, x: Numeric, y: Numeric):
        self.x = Decimal(x)
        self.y = Decimal(y)

    @property
    def xy(self):
        return (self.x, self.y)

    def __getitem__(self, value):
        return self.xy[value]

    def __setitem__(self, key, value):
        self.xy[key] = value


class PhysicsObject:
    def __init__(self, box: Rect, sprite: Surface, *, stable_angles = [0]):
        self.box = box
        self._sprite = sprite

        self.stable_angles = stable_angles

        self._velocity = Point2D(0, 0)
        self.rotation = Decimal(0.0)
        self.weight = 1

        self._on_floor = False
        self.next_stable = None
        self.clockwise = True

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if isinstance(value, Point2D):
            self._velocity = value
        else:
            self._velocity = Point2D(value[0], value[1])

    @property
    def center(self):
        return self.box.center

    @property
    def sprite(self):
        s = pygame.transform.rotozoom(self._sprite, self.rotation, 1)
        return s

    def update(self):
        self.rotation %= 360
        self.rotation = round(self.rotation, 3)
        if self._on_floor:
            self.velocity = (0, 0)
            if self.rotation not in self.stable_angles:
                self.next_stable = get_closest(self.rotation, self.stable_angles)
                self.clockwise = self.next_stable >= self.rotation
        if self.next_stable is not None:
            if self.clockwise:
                self.rotation += self.weight
                if self.rotation >= self.next_stable:
                    self.rotation = self.next_stable
                    self.next_stable = None
            else:
                self.rotation -= self.weight
                if self.rotation < self.next_stable:
                    self.rotation = self.next_stable
                    self.next_stable = None

        self.box.x += self.velocity.x
        self.box.y += self.velocity.y

    def render_to(self, surface: Surface):
        surface.blit(self.sprite, self.box)


class PhysicsRoom:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surface = Surface((width, height))

        self.objects: List[PhysicsObject] = []

        self.resolution = 5  # px/m
        self.gravity = Decimal(9.8)
        self.tick_rate = 120

    def update(self):
        for obj in self.objects:
            if obj.box.bottom >= self.height:
                obj._on_floor = True
                obj.box.bottom = self.height - 1
            if obj._on_floor is False:
                obj.velocity.y += (self.gravity * self.resolution) / self.tick_rate
        for obj in self.objects:
            obj.update()

    def render(self):
        self.surface.fill("clear")
        for obj in self.objects:
            obj.render_to(self.surface)
