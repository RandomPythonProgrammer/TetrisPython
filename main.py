import random
import time
from copy import deepcopy

import pyglet

from piece import Piece, PieceType


class Game(pyglet.window.Window):
    def __init__(self, width, height):
        super(Game, self).__init__(width, height)
        self.scale = width / 10
        self.board = []
        self.grace_frame = 2
        self.max_grace = 2
        for i in range(20):
            lst = []
            for j in range(10):
                lst.append(0)
            self.board.append(lst)
        self.piece = Piece(PieceType(random.randint(1, 7)))
        self.start_time = self.last_time = time.time()
        self.level = 0
        self.points = 0
        self.line_clears = 0
        self.since_i = 1 if self.piece.piece_type is PieceType.I else 0
        self.theme = pyglet.media.load('assets/theme.wav')
        self.media_player = pyglet.media.Player()
        self.media_player.loop = True
        self.media_player.queue(self.theme)
        self.media_player.play()
        self.pressed_keys = {}
        self.controller = None
        controllers = pyglet.input.get_controllers()
        if len(controllers) > 0:
            self.controller = controllers[0]
            self.controller.open()
            self.controller.on_button_press = self.on_button_press

        self.paused = False

    def on_update(self, dt):
        if not self.paused:
            if (time.time() - self.last_time > 0.1 and (
                    (pyglet.window.key.S in self.pressed_keys and self.pressed_keys[pyglet.window.key.S]) or (
                    self.controller is not None and self.controller.a))) \
                    or (time.time() - self.last_time >= 1 - min(0.9, (self.level ** 0.75) * 0.15)):
                self.last_time = time.time()
                if self.piece is not None:
                    self.move_piece(0, -1)
            self.set_caption(f'[Tetris] Level: {self.level} Score: {self.points}')

    def rotate_left(self):
        temp = deepcopy(self.piece)
        for i in range(len(temp.matrix)):
            for j in range(len(temp.matrix[i])):
                temp.matrix[i][j] = self.piece.matrix[j][len(temp.matrix[j]) - 1 - i]
        if self.check_placement(temp):
            self.piece = temp
            self.grace_frame += 1
            if self.grace_frame > self.max_grace:
                self.grace_frame = self.max_grace

    def rotate_right(self):
        temp = deepcopy(self.piece)
        for i in range(len(temp.matrix)):
            for j in range(len(temp.matrix[i])):
                temp.matrix[i][j] = self.piece.matrix[len(temp.matrix) - 1 - j][i]
        if self.check_placement(temp):
            self.piece = temp
            self.grace_frame += 1
            if self.grace_frame > self.max_grace:
                self.grace_frame = self.max_grace

    def check_placement(self, piece):
        for i in range(len(piece.matrix)):
            for j in range(len(piece.matrix[i])):
                if piece.matrix[i][j] != 0:
                    column = piece.x + j
                    row = 20 - piece.y - len(piece.matrix) + i
                    if (row >= 0 and (row >= len(self.board))) \
                            or (0 > column or column >= len(self.board[row])) \
                            or self.board[row][column] != 0:
                        return False
        return True

    def move_piece(self, dx, dy):
        temp = deepcopy(self.piece)
        temp.x += dx
        temp.y += dy
        if self.check_placement(temp):
            self.piece = temp
        elif dy != 0:
            if self.grace_frame <= 0:
                self.kill_piece()
                self.grace_frame = 2
            else:
                self.grace_frame -= 1
        elif dx != 0:
            self.grace_frame += 1
            if self.grace_frame > self.max_grace:
                self.grace_frame = self.max_grace

    def kill_piece(self):
        for i in range(len(self.piece.matrix)):
            for j in range(len(self.piece.matrix[i])):
                if self.piece.matrix[i][j] != 0:
                    column = self.piece.x + j
                    row = 20 - self.piece.y - len(self.piece.matrix) + i
                    self.board[row][column] = self.piece.matrix[i][j]

        cleared_lines = 0
        i = len(self.board) - 1
        while i >= 0:
            if 0 not in self.board[i]:
                temp = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                temp.extend(self.board[:i])
                if i < len(self.board) - 1:
                    temp.extend(self.board[i + 1:])
                cleared_lines += 1
                i = len(self.board)
                self.board = temp
            i -= 1

        if (self.line_clears % 10) + cleared_lines >= 10:
            self.level += 1
        self.line_clears += cleared_lines

        if cleared_lines == 1:
            self.points += 40 * (self.level + 1)
        elif cleared_lines == 2:
            self.points += 100 * (self.level + 1)
        elif cleared_lines == 3:
            self.points += 300 * (self.level + 1)
        elif cleared_lines == 4:
            self.points += 1200 * (self.level + 1)

        if self.since_i >= 6:
            piece = PieceType.I
            self.since_i = 0
        else:
            piece = PieceType(random.randint(1, 7))
            if piece is not PieceType.I:
                self.since_i += 1
        self.piece = Piece(piece)

        for i in range(len(self.piece.matrix)):
            for j in range(len(self.piece.matrix[i])):
                if self.piece.matrix[i][j] != 0:
                    column = self.piece.x + j
                    row = 20 - self.piece.y - len(self.piece.matrix) + i
                    if self.board[row][column] != 0:
                        self.close()

    def on_button_press(self, controller, button_name):
        if button_name == 'x':
            self.on_key_press(pyglet.window.key.A, None)
        elif button_name == 'b':
            self.on_key_press(pyglet.window.key.D, None)
        elif button_name == 'a':
            self.on_key_press(pyglet.window.key.SPACE, None)
        elif button_name == 'leftshoulder':
            self.on_key_press(pyglet.window.key.Q, None)
        elif button_name == 'rightshoulder':
            self.on_key_press(pyglet.window.key.E, None)

    def on_key_press(self, symbol, modifiers):
        if symbol is pyglet.window.key.Q:
            if self.controller is not None:
                self.controller.rumble_play_weak(duration=0.1)
            self.rotate_left()
        elif symbol is pyglet.window.key.E:
            if self.controller is not None:
                self.controller.rumble_play_weak(duration=0.1)
            self.rotate_right()
        if symbol is pyglet.window.key.A:
            if self.controller is not None:
                self.controller.rumble_play_weak(duration=0.1)
            self.move_piece(-1, 0)
        elif symbol is pyglet.window.key.D:
            if self.controller is not None:
                self.controller.rumble_play_weak(duration=0.1)
            self.move_piece(1, 0)
        elif symbol is pyglet.window.key.SPACE:
            if self.controller is not None:
                self.controller.rumble_play_strong(duration=0.2)
            temp = deepcopy(self.piece)
            while self.check_placement(temp):
                self.piece = deepcopy(temp)
                temp.y -= 1
            self.kill_piece()
        elif symbol is pyglet.window.key.P:
            self.paused = not self.paused
        self.pressed_keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        self.pressed_keys[symbol] = False

    def on_render(self, dt):
        self.clear()
        if self.piece is not None:
            for i in range(len(self.piece.matrix)):
                for j in range(len(self.piece.matrix[i])):
                    if i < len(self.board) and j < len(self.board[i]):
                        value = self.piece.matrix[i][j]
                        if value != 0:
                            x = (self.piece.x + j) * self.scale
                            y = (self.piece.y + (len(self.piece.matrix) - i - 1)) * self.scale
                            rectangle = pyglet.shapes.Rectangle(
                                x, y,
                                self.scale, self.scale,
                                PieceType.get_color(PieceType(value))
                            )
                            rectangle.draw()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                value = self.board[i][j]
                if value != 0:
                    x = j * self.scale
                    y = (20 - 1 - i) * self.scale
                    rectangle = pyglet.shapes.Rectangle(
                        x, y,
                        self.scale, self.scale,
                        PieceType.get_color(PieceType(value))
                    )
                    rectangle.draw()

        ghost = deepcopy(self.piece)
        while True:
            ghost.y -= 1
            if not self.check_placement(ghost):
                ghost.y += 1
                break

        for i in range(len(ghost.matrix)):
            for j in range(len(ghost.matrix[i])):
                value = ghost.matrix[i][j]
                if value != 0:
                    x = (ghost.x + j) * self.scale
                    y = (ghost.y + (len(ghost.matrix) - i - 1)) * self.scale
                    rectangle = pyglet.shapes.Rectangle(
                        x, y,
                        self.scale, self.scale,
                        PieceType.get_color(PieceType(value))
                    )
                    rectangle.opacity = 75
                    rectangle.draw()


if __name__ == '__main__':
    display = pyglet.canvas.Display().get_default_screen()
    x_mult, y_mult = display.width / 10, display.height / 20
    mult = round(min(x_mult, y_mult) * 0.75)
    game = Game(10 * mult, 20 * mult)
    pyglet.clock.schedule(game.on_update)
    pyglet.clock.schedule(game.on_render)
    pyglet.app.run()
