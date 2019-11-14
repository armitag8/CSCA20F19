#! /usr/bin/env python3
import turtle
import random
from functools import total_ordering, partial
from tkinter import messagebox, Toplevel, Label
import os
import sys
import const
import score_board_db


def main():
    Game().start()


@total_ordering
class _AbstractFish(turtle.Turtle):
    SHAPE_NAME = "fish"
    SHAPE = turtle.Shape("polygon",
                         (
                             (3, -4), (2, -3), (1, -2), (2, -1), (3, 0),
                             (3, 1), (2, 3), (1, 4), (0, 3),
                             (-1, 4), (-2, 3), (-3, 1), (-3, 0),
                             (-2, -1), (-1, -2), (-2, -3), (-3, -4),
                         )
                         )
    BASE_SIZE = 3.75

    def __init__(self, speed: int, size: int, position: tuple):
        super().__init__()
        self._fish_speed = speed
        self.speed(10)
        self.penup()
        self.recreate(size, position)

    def __eq__(self, other: "Fish") -> bool:
        """Is this fish the same size as the other?"""
        return self._fish_size == other._fish_size

    def __lt__(self, other: "Fish") -> bool:
        """Is this fish smaller in size compared to  the other?"""
        return self._fish_size < other._fish_size

    def touching(self, other: "Fish") -> bool:
        """Is this fish touching the other"""
        radius = (self._fish_size + other._fish_size) * self.BASE_SIZE - 1
        return self.is_in_radius(other, radius)

    def is_in_radius(self, other: "Fish", radius: int) -> bool:
        """Is this fish within radius pixels of the other?"""
        self_x, self_y = self.position()
        other_x, other_y = other.position()
        return (self_x - other_x) ** 2 + (self_y - other_y) ** 2 < radius ** 2

    def get_size(self) -> int:
        """Returns the size of this fish."""
        return self._fish_size

    def get_speed(self):
        """Returns the speed of this fish."""
        return self._fish_speed

    def recreate(self, size: int, position: tuple):
        """Recreates this fish with new size and position."""
        self._fish_size = size
        self.shape(self.SHAPE_NAME)
        self.shapesize(self._fish_size, self._fish_size)
        self.hideturtle()
        self.setposition(*position)
        self.showturtle()

    def move(self, step=None):
        """Moves this fish forwards step, if given, else by its speed."""
        if step is not None:
            self.forward(step)
        else:
            self.forward(self.get_speed())

    def is_off_screen(self) -> bool:
        """Has this fish left the screen / ocean?"""
        x, y = self.position()
        return abs(x) > Ocean.MAX_X or abs(y) > Ocean.MAX_Y


class NPCFish(_AbstractFish):
    def __init__(self, speed: int, size: int, position: tuple):
        super().__init__(speed, size, position)
        self.color("green")

    def get_speed(self):
        """Randomly gives a speed between 1/3 of base and full base speed."""
        return random.randrange(1, 3) * self._fish_speed / 3

    def random_move(self):
        """Randomly change heading and move forward."""
        self.right(random.randint(-20, 20))
        self.move()
        if self.is_off_screen():
            self.setheading(self.towards((0, 0)))

    @staticmethod
    def random_spawn(speed: int, size: int) -> "Fish":
        """Create a new NPCFish in a random location with random stats."""
        fish = NPCFish(speed * random.randint(1, 3),
                       size * random.random(),
                       Ocean.get_random_coordinates())
        fish.setheading(random.randint(0, 360))
        return fish


class PlayerFish(_AbstractFish):
    def __init__(self, speed: int, size: int):
        """Create a new fish for player to control and bind keys and mouse"""
        super().__init__(speed, size, (0, 0))
        self.color("gold")

        screen = turtle.Screen()

        def set_mouse(state: bool, x: int, y: int):
            self._mouse = state
            self._mouse_x = x
            self._mouse_y = y
        self._mouse = False
        screen.onclick(partial(set_mouse, True))

        def set_direction_key(key: str, state: bool):
            self._buttons[key] = state
            self._mouse = False
        self._buttons = {d: False for d in ("Up", "Down", "Left", "Right")}
        for d in self._buttons:
            screen.onkeypress(partial(set_direction_key, d, True), d)
            screen.onkeyrelease(partial(set_direction_key, d, False), d)

    def controlled_move(self):
        """Move according to pressed keys or last position clicked on screen."""
        step = self.get_speed()

        right = self._buttons["Right"]
        up = self._buttons["Up"]
        left = self._buttons["Left"]
        down = self._buttons["Down"]

        if self._mouse:
            self.setheading(self.towards(self._mouse_x, self._mouse_y))
        elif right and not up and not left and not down:
            self.setheading(0)
        elif right and up and not left and not down:
            self.setheading(45)
        elif not right and up and not left and not down:
            self.setheading(90)
        elif not right and up and left and not down:
            self.setheading(135)
        elif not right and not up and left and not down:
            self.setheading(180)
        elif not right and not up and left and down:
            self.setheading(225)
        elif not right and not up and not left and down:
            self.setheading(270)
        elif right and not up and not left and down:
            self.setheading(315)
        else:
            step = 0

        self.move(step)

        if self.is_off_screen():
            raise GameOver("You left the ocean :(")

    def eat(self, other: "Fish"):
        """Attempt to eat the other Fish. Raise an Error if it's too big."""
        if self > other:
            SoundEngine().play_effect("eat")
            p_size = self.get_size()
            new_player_size = p_size + other.get_size() / p_size
            self.recreate(new_player_size, self.position())
            other.recreate(random.randint(self.get_size() // 1.5,
                                          int(self.get_size() * 1.5)),
                           Ocean.get_random_coordinates(avoid=self.position(),
                                                        margin=self.get_size() * 10))
        else:
            raise GameOver("You were eaten :(")


class Ocean:
    MAX_X = 512
    MAX_Y = 384

    def __init__(self):
        """Create a new Ocean."""
        self._window = turtle.Screen()
        self._window.screensize(self.MAX_X * 2, self.MAX_Y * 2, "blue")
        self._window.title(Game.TITLE)
        self._window.register_shape(_AbstractFish.SHAPE_NAME,
                                    _AbstractFish.SHAPE)
        self.reset_fish()

    def reset_fish(self):
        """Rebuild all NPC and PLayer fish."""
        self._window.clearscreen()
        self._window.bgpic(const.BACKGROUND)
        self._window.listen()
        self._window.delay(0)

        self._player = self.make_player()
        self._fishes = self.make_fish()

    def make_fish(self) -> list:
        """Get a list of new NPC fish."""
        return [
            NPCFish.random_spawn(const.BASE_FISH_SPEED, const.BASE_FISH_SIZE)
            for i in range(const.NUM_FISH)
        ]

    def make_player(self) -> PlayerFish:
        """Get a new Player Fish."""
        return PlayerFish(const.PLAYER_SPEED, const.PLAYER_START_SIZE)

    def get_screen(self) -> turtle.Screen:
        return self._window

    def move_all_fish(self):
        """Move all fish on screen (called for each update / frame generated)"""
        self._player.controlled_move()
        for fish in self._fishes:
            if fish.touching(self._player):
                self._player.eat(fish)
            fish.random_move()

    @staticmethod
    def get_random_coordinates(avoid: tuple = (0, 0), margin: int = 20) -> tuple:
        """Get random coordinates not too near the player."""
        self_x, self_y = avoid
        while True:
            x = random.randint(-Ocean.MAX_X, Ocean.MAX_X)
            y = random.randint(-Ocean.MAX_Y, Ocean.MAX_Y)
            if abs(self_x - x) > margin and abs(self_y - y) > margin:
                break
        return x, y

    def get_player(self):
        return self._player


class SoundEngine:
    class __SoundEngine:
        # Ghetto workaround to fix pygame's import nonsense (printing)
        old_target = sys.stdout
        devnull_target = open(os.devnull, 'w')
        sys.stdout = devnull_target
        from pygame import mixer
        sys.stdout = old_target

        def __init__(self):
            self.mixer.init()
            self.mixer.music.load(const.MUSIC)
            self._playing = False
            self._muted = False

    instance = None

    def __init__(self):
        if SoundEngine.instance is None:
            SoundEngine.instance = SoundEngine.__SoundEngine()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        setattr(self.instance, name, value)

    def play(self):
        if not self._muted:
            self._playing = True
            self.mixer.music.play(-1)

    def toggle_mute(self, is_running: bool):
        self._muted = not self._muted
        if is_running:
            self.toggle_pause()

    def toggle_pause(self):
        if self._playing:
            self.mixer.music.pause()
            self._playing = False
        else:
            self.play()

    def game_over(self):
        self.mixer.music.stop()
        self._playing = False
        self.play_effect("game_over")

    def play_effect(self, effect: str):
        if not self._muted:
            self.mixer.Sound(const.EFFECTS[effect]).play()


class Game:
    TITLE = "Bigger Fish"

    def __init__(self):
        self._ocean = Ocean()
        self._sounds = SoundEngine()

    def start(self):
        """Begin main loop of game; action on screen begins."""
        screen = self._ocean.get_screen()
        screen.onkey(self.pause, "Escape")
        screen.onkey(self.mute, "m")
        self._sounds.play()
        self._running = True
        self.run()
        screen.mainloop()

    def restart(self):
        """Reset and restart the game."""
        self._ocean.reset_fish()
        self.start()

    def pause(self):
        """Pause the game."""
        self._sounds.toggle_pause()
        self._running = not self._running

    def mute(self):
        """Mute all sounds in game"""
        self._sounds.toggle_mute(self._running)

    def run(self):
        """Main logic of game: runs once per frame / update."""
        try:
            if self._running:
                self._ocean.move_all_fish()
        except GameOver as e:
            self._running = False
            self._sounds.game_over()
            self.restart_prompt(str(e))
        except turtle.Terminator:
            self._sounds.game_over()
        except Exception as e:
            self._sounds.game_over()
        else:
            self._ocean.get_screen().ontimer(self.run, 16)  # 16.77 ms => 60 FPS

    def restart_prompt(self, title: str):
        """Opens ScoreBoard, and asks Player to play again."""
        score_board = ScoreBoard()
        score_board.record_score(self.get_score())
        response = messagebox.askyesno(title, "Would you like to play again?")
        score_board.destroy()
        if response:
            self.restart()
        else:
            self._ocean.get_screen().bye()

    def get_score(self) -> int:
        """Get the current score of the Player"""
        return int(self._ocean.get_player().get_size() * 500)


class GameOver(Exception):
    def __init__(self, message: str):
        super().__init__("Game Over: " + message)


class ScoreBoard:
    def __init__(self):
        self.show_scores(score_board_db.get_highscores())

    def show_scores(self, scores: list):
        self._board = Toplevel()
        self._board.title("High Scores")
        for i, row in enumerate([("Name", "Score", "Date")] + scores):
            for j in range(3):
                Label(self._board, text=row[j]).grid(row=i,
                                                     column=j, padx=30, pady=10)

    def record_score(self, score: int):
        highscores = score_board_db.get_highscores()
        new_highscore = not len(highscores) == 10 or score > highscores[-1][1]
        if new_highscore:
            message = "New High Score!"
        else:
            message = "Sorry, try again."
        name = turtle.Screen().textinput(message, "Input your name: ")
        if name:
            score_board_db.add_score(name, score)
            if new_highscore:
                scores = score_board_db.get_highscores()
            else:
                scores = score_board_db.get_scores_near(score)
            self._board.destroy()
            self.show_scores(scores)

    def destroy(self):
        self._board.destroy()


if __name__ == "__main__":
    if not os.path.isfile(const.DB_FILE):
        score_board_db.initialize_score_db()
    main()
