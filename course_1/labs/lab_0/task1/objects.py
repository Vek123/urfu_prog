__all__ = []

import abc
from dataclasses import dataclass
import datetime
from typing import Any, Callable, Optional

import pygame

from exceptions import GameOver, NextLevel, Win
from settings import DISPLAY_RESOLUTION

CURRENT_EVENTS = []


class Screenable(abc.ABC):
    @property
    @abc.abstractmethod
    def on_screen(self) -> bool: ...

    @abc.abstractmethod
    def show(self, screen: pygame.surface.Surface) -> None: ...

    @abc.abstractmethod
    def hide(self) -> None: ...

    @abc.abstractmethod
    def clear(self) -> None: ...


class Playable(abc.ABC):
    @property
    @abc.abstractmethod
    def player(self) -> "Player": ...


class Collidable(abc.ABC):
    @property
    @abc.abstractmethod
    def rect(self) -> pygame.Rect: ...

    @abc.abstractmethod
    def is_collide(self, obj: "Collidable") -> bool: ...


class Movable(abc.ABC):
    @property
    @abc.abstractmethod
    def only_on_screen(self) -> bool: ...

    @abc.abstractmethod
    def move(self, x: float, y: float) -> None: ...


class Game:
    def __init__(self, screen: pygame.surface.Surface, framerate: int = 60):
        self.current_level = 1
        self.levels: list[Screenable] = [
            Level1(),
            Level2,
            WinMap,
        ]
        self.screen = screen
        self.framerate = framerate
        self.clock = pygame.time.Clock()
        self.objects_on_screen = set()
        self.win_time = None

    def frame(self) -> None:
        self._handle_entities()
        self.levels[self.current_level].show(self.screen)

    def start(self) -> None:
        pygame.init()
        self.before_start()
        pygame.display.flip()
        while True:
            CURRENT_EVENTS[:] = pygame.event.get()
            for event in CURRENT_EVENTS:
                if event.type == pygame.QUIT:
                    self.stop()
                    pygame.quit()
                    raise SystemExit()

            self.screen.fill("white")
            if self.win_time:
                if datetime.datetime.now() - self.win_time > datetime.timedelta(seconds=10):
                    self.win_time = None
                    self._go_to_level(0)

                self.levels[self.current_level].show(self.screen)
                pygame.display.flip()
                self.clock.tick(self.framerate)
                continue

            try:
                self.frame()
                pygame.display.flip()
                self.clock.tick(self.framerate)
            except GameOver:
                self._go_to_level(self.current_level)
                self.clock.tick(self.framerate)
            except NextLevel:
                self._go_to_level(self.current_level + 1)
            except Win:
                self._go_to_level(len(self.levels)-1)
                self.win_time = datetime.datetime.now()
                pygame.display.flip()
                self.clock.tick(self.framerate)

    def before_start(self) -> None: ...

    def stop(self) -> None: ...

    def add_object_to_screen(self, obj: Screenable) -> None:
        obj.show(self.screen)
        self.objects_on_screen.add(obj)

    def remove_object_from_screen(self, obj: Screenable) -> None:
        obj.hide()
        self.objects_on_screen.remove(obj)

    def _handle_entities(self) -> None:
        for entity in Entity.entities_by_id.values():
            entity.frame()

    def _init_level(self, level: int):
        self.levels[level] = self.levels[level]()

    def _go_to_level(self, level: int):
        self.levels[self.current_level].clear()
        self.levels[self.current_level].hide()
        self.levels[self.current_level] = type(self.levels[level])
        self.current_level = level
        self._init_level(self.current_level)
        self.levels[level].on_screen = True


@dataclass
class Route:
    coords: tuple[int, int]
    prev: Optional["Route"] = None
    next: Optional["Route"] = None  # noqa


class Entity(Screenable, Collidable):
    rect: pygame.Rect = None
    img: pygame.surface.Surface = None
    on_screen: bool = True
    entities_by_id: dict[int, "Entity"] = {}
    alive: bool = True
    __next_id: int = 0

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Any,
        img_path: str | None = None,
        frame_callback: Callable | None = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.id = Entity.__next_id
        Entity.__next_id += 1
        self.frame_callback = frame_callback
        Entity.entities_by_id[self.id] = self
        if img_path:
            img = pygame.image.load(img_path).convert_alpha()
            self.img = pygame.transform.scale(img, (self.width, self.height))
            rect = self.img.get_rect(
                left=self.left,
                top=self.top,
                width=self.width,
                height=self.height,
            )
        else:
            rect = pygame.Rect(
                self.left,
                self.top,
                self.width,
                self.height,
            )

        rect.center = (self.x, self.y)
        self.rect = rect

    def clear(self):
        self.entities_by_id.pop(self.id)
        self.alive = False

    @property
    def left(self) -> float:
        return self.x - self.width // 2

    @property
    def top(self) -> float:
        return self.y - self.height // 2

    def is_collide(self, obj: "Entity") -> bool:
        if not self.on_screen:
            return False

        return self.rect.colliderect(obj.rect)

    def show(self, screen: pygame.surface.Surface) -> None:
        if not self.on_screen:
            return

        if self.img:
            screen.blit(self.img, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def hide(self) -> None:
        self.on_screen = False

    def frame(self):
        if self.alive and self.frame_callback:
            self.frame_callback(self)


class Wall(Entity):
    walls_by_id: dict[int, "Wall"] = {}

    def __init__(self, x, y, width, height, color, img_path=None, frame_callback=None):
        super().__init__(x, y, width, height, color, img_path, frame_callback)
        self.walls_by_id[self.id] = self

    def clear(self):
        self.walls_by_id.pop(self.id)
        super().clear()


class MovableEntity(Entity, Movable):
    only_on_screen: bool = True
    movable_entities_by_id: dict[int, "MovableEntity"] = {}

    def __init__(
        self,
        x,
        y,
        width,
        height,
        color,
        img_path=None,
        frame_callback=None,
        route: Route | None = None,
        on_route: bool = False,
        speed: int = 10,
    ):
        super().__init__(x, y, width, height, color, img_path, frame_callback)
        self.movable_entities_by_id[self.id] = self
        self.route = route
        self.on_route = on_route
        self.speed = speed

    def clear(self):
        self.movable_entities_by_id.pop(self.id)
        super().clear()

    def move(self, x: float, y: float):
        if not self.on_screen:
            return

        if self.only_on_screen:
            next_top = self.top + y
            next_bottom = self.top + self.height + y
            next_left = self.left + x
            next_right = self.left + self.width + x
            if next_top < 0:
                y += abs(next_top)
            elif next_bottom > DISPLAY_RESOLUTION[1]:
                y -= next_bottom - DISPLAY_RESOLUTION[1]

            if next_left < 0:
                x += abs(next_left)
            elif next_right > DISPLAY_RESOLUTION[0]:
                x -= next_right - DISPLAY_RESOLUTION[0]

        old_rect = self.rect
        self.rect = self.rect.move(x, y)
        for wall in Wall.walls_by_id.values():
            if wall.is_collide(self):
                self.rect = old_rect
                return

        self.x += x
        self.y += y

    def frame(self):
        if self.on_screen and self.on_route and self.route:
            if self.rect.center != self.route.coords:
                x_dist = self.route.coords[0] - self.x
                y_dist = self.route.coords[1] - self.y
                x_move = min(self.speed, x_dist) if x_dist >= 0 else max(-self.speed, x_dist)
                y_move = min(self.speed, y_dist) if y_dist >= 0 else max(-self.speed, y_dist)
                self.move(x_move, y_move)
            else:
                self.route = self.route.next

        super().frame()


class Enemy(MovableEntity):
    pass


class EnemyTouch(Enemy):
    def frame(self):
        if self.on_screen:
            for player in Player.players_by_id.values():
                if self.rect.colliderect(player.rect):
                    raise GameOver()

        super().frame()


class Player(MovableEntity):
    players_by_id: dict[str, "Player"] = {}

    def __init__(
        self,
        left,
        top,
        width,
        height,
        color,
        img_path=None,
        frame_callback=None,
    ):
        super().__init__(
            left,
            top,
            width,
            height,
            color,
            img_path,
            frame_callback,
        )
        self.players_by_id[self.id] = self

    def clear(self):
        self.players_by_id.pop(self.id)
        super().clear()

    def frame(self):
        self.handle_keyboard()
        super().frame()

    def handle_keyboard(self):
        if self.on_screen:
            keys = pygame.key.get_pressed()
            y, x = 0, 0
            if keys[pygame.K_UP]:
                y += -self.speed

            if keys[pygame.K_DOWN]:
                y += self.speed

            if keys[pygame.K_LEFT]:
                x += -self.speed

            elif keys[pygame.K_RIGHT]:
                x += self.speed

            if x and y:
                new_speed = (self.speed**2 / 2) ** (1 / 2)
                x = new_speed if x > 0 else -new_speed
                y = new_speed if y > 0 else -new_speed

            self.move(x, y)


class Level1(Playable, Screenable):
    on_screen: bool = True
    player: Player = None

    def __init__(self):
        super().__init__()
        self.player = self.create_player()
        self.walls = self.create_walls()
        self.entities = self.create_entities()

    def clear(self):
        self.player.clear()
        for wall in self.walls:
            wall.clear()

        for entity in self.entities:
            entity.clear()

    def create_walls(self) -> list[Wall]:
        return [
            Wall(102, 250, 5, 400, "black"),
            Wall(500, 602, 800, 5, "black"),
            Wall(902, 327, 5, 555, "black"),
            Wall(500, 52, 800, 5, "black"),
            Wall(400, 452, 600, 5, "black"),
            Wall(702, 125, 5, 150, "black"),
            Wall(702, 402, 5, 105, "black"),
        ]

    def create_entities(self) -> list[Entity]:
        def create_enemy() -> EnemyTouch:
            start_route = Route((810, 202))
            start_route.next = Route((810, 500))
            start_route.next.next = start_route

            return EnemyTouch(
                810,
                202,
                120,
                105,
                "black",
                "../assets/monster_3.png",
                route=start_route,
                on_route=True,
                speed=5,
            )

        def create_key() -> Entity:
            def frame(key: Entity):
                player = self.player
                if key.rect.colliderect(player.rect):
                    key.hide()
                    door.hide()
                    door_opened.on_screen = True

            return Entity(
                795,
                105,
                50,
                50,
                "black",
                "../assets/key.png",
                frame,
            )

        def create_graal() -> Entity:
            def frame(graal: Entity):
                player = self.player
                if graal.rect.colliderect(player.rect):
                    raise NextLevel()

            return Entity(
                400,
                300,
                100,
                100,
                "black",
                "../assets/graal.png",
                frame,
            )

        door = Wall(
            702,
            272,
            5,
            145,
            "brown",
        )
        door_opened = Wall(
            627,
            202,
            145,
            5,
            "brown",
        )
        door_opened.hide()

        return [create_enemy(), door, door_opened, create_key(), create_graal()]

    def create_player(self) -> Player:
        return Player(
            10,
            10,
            40,
            30,
            "black",
            "../assets/red_ball.png",
        )

    def show(self, screen: pygame.surface.Surface) -> None:
        if not self.on_screen:
            return

        self.player.show(screen)
        for wall in self.walls:
            wall.show(screen)

        for entity in self.entities:
            entity.show(screen)

    def hide(self) -> None:
        self.on_screen = False


class Level2(Playable, Screenable):
    on_screen: bool = True
    player: Player = None

    def __init__(self):
        super().__init__()
        self.player = self.create_player()
        self.walls = self.create_walls()
        self.entities = self.create_entities()

    def clear(self):
        self.player.clear()
        for wall in self.walls:
            wall.clear()

        for entity in self.entities:
            entity.clear()

    def create_walls(self) -> list[Wall]:
        return [
            Wall(102, 250, 5, 400, "black"),
            Wall(500, 602, 800, 5, "black"),
            Wall(902, 327, 5, 555, "black"),
            Wall(500, 52, 800, 5, "black"),
            Wall(400, 452, 600, 5, "black"),
            Wall(702, 125, 5, 150, "black"),
            Wall(702, 402, 5, 105, "black"),
        ]

    def create_entities(self) -> list[Entity]:
        def create_enemy() -> EnemyTouch:
            start_route = Route((810, 202))
            start_route.next = Route((810, 500))
            start_route.next.next = start_route

            return EnemyTouch(
                810,
                202,
                120,
                105,
                "black",
                "../assets/monster_3.png",
                route=start_route,
                on_route=True,
                speed=5,
            )

        def create_key() -> Entity:
            def frame(key: Entity):
                player = self.player
                if key.rect.colliderect(player.rect):
                    key.hide()
                    door.hide()
                    door_opened.on_screen = True

            return Entity(
                795,
                105,
                50,
                50,
                "black",
                "../assets/key.png",
                frame,
            )

        def create_graal() -> Entity:
            def frame(graal: Entity):
                player = self.player
                if graal.rect.colliderect(player.rect):
                    raise Win()

            return Entity(
                400,
                300,
                100,
                100,
                "black",
                "../assets/graal.png",
                frame,
            )

        def create_enemy2() -> EnemyTouch:
            def frame(enemy: EnemyTouch) -> None:
                if datetime.datetime.now() - enemy._last_active > datetime.timedelta(seconds=2):
                    spikes.hide()
                    enemy._last_active = datetime.datetime.now()
                elif datetime.datetime.now() - enemy._last_active > datetime.timedelta(seconds=1):
                    spikes.on_screen = True

            spikes = EnemyTouch(
                600,
                530,
                200,
                200,
                "black",
                "../assets/spikes.png",
                frame_callback=frame,
            )
            spikes._last_active = datetime.datetime.now()
            spikes.hide()
            return spikes

        door = Wall(
            702,
            272,
            5,
            145,
            "brown",
        )
        door_opened = Wall(
            627,
            202,
            145,
            5,
            "brown",
        )
        door_opened.hide()

        return [create_enemy(), create_enemy2(), door, door_opened, create_key(), create_graal()]

    def create_player(self) -> Player:
        return Player(
            10,
            10,
            40,
            30,
            "black",
            "../assets/red_ball.png",
        )

    def show(self, screen: pygame.surface.Surface) -> None:
        if not self.on_screen:
            return

        self.player.show(screen)
        for wall in self.walls:
            wall.show(screen)

        for entity in self.entities:
            entity.show(screen)

    def hide(self) -> None:
        self.on_screen = False


class WinMap(Screenable):
    on_screen: bool = False

    def __init__(self):
        super().__init__()
        self.title = Entity(
            DISPLAY_RESOLUTION[0] // 2,
            DISPLAY_RESOLUTION[1] // 2,
            1280,
            720,
            "black",
            "../assets/win.png",
        )

    def clear(self) -> None:
        self.title.clear()

    def show(self, screen: pygame.surface.Surface) -> None:
        if not self.on_screen:
            return

        self.title.show(screen)

    def hide(self) -> None:
        self.on_screen = False
