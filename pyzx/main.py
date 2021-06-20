from pyzx.pyzx import PhysicsObject, PhysicsRoom
import nygame

from pygame import Rect, Surface


class Box(PhysicsObject):
    def __init__(self, box: Rect):
        sprite = Surface((box.w, box.h))
        sprite.fill("red")
        super().__init__(box, sprite, stable_angles = [0, 90, 180, 270, 360])


class Game(nygame.Game):
    def __init__(self):
        super().__init__(size = (1280, 720), fps = 120, showfps = True)
        self.room = PhysicsRoom(1280, 720)
        self.box = Box(Rect(400, 100, 100, 100))
        self.box.rotation = 20

        self.room.objects.append(self.box)

    def render_room(self):
        self.room.render()
        self.surface.blit(self.room.surface, (0, 0))

    def loop(self, events):
        for event in events:
            pass

        self.room.update()

        self.render_room()


def main():
    Game().run()


if __name__ == "__main__":
    main()
