from decimal import Decimal
from typing import Union

from pygame import Rect, Surface
import pygame.transform

Numeric = Union[Decimal, int, float]
GenericPoint2D = tuple[Numeric, Numeric]

PX_PER_M = 100


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
    def __init__(self, box: Rect, sprite: Surface):
        self.box = box
        self._sprite = sprite

        self.velocity = Point2D(0, 0)
        self.rotation = 0.0

    @property
    def sprite(self):
        s = pygame.transform.rotozoom(self._sprite, self.rotation, 1)
        return s

    def update(self):
        pass

    def render_to(self, surface: Surface):
        surface.blit(self.sprite, self.box)


class PhysicsRoom:
    def __init__(self, width: int, height: int):
        pass
