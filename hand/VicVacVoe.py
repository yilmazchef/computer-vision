import random
from os import walk

import cv2
import time
from keyboard import write, press_and_release, wait
import pyglet

from screeninfo import get_monitors
from cvzone.HandTrackingModule import HandDetector

import random


class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def get_random_first_player(self):
        return random.randint(0, 1)

    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    def is_player_win(self, player):
        win = None

        n = len(self.board)

        # checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start(self):
        self.create_board()

        player = 'X' if self.get_random_first_player() == 1 else 'O'
        while True:
            print(f"Player {player} turn")

            self.show_board()

            # taking user input
            row, col = list(
                map(int, input("Enter row and column numbers to fix spot: ").split()))
            print()

            # fixing the spot
            self.fix_spot(row - 1, col - 1, player)

            # checking whether current player is won or not
            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            # checking whether the game is draw or not
            if self.is_board_filled():
                print("Match Draw!")
                break

            # swapping the turn
            player = self.swap_player_turn(player)

        # showing the final view of board
        print()
        self.show_board()


# starting the game
# tic_tac_toe = TicTacToe()
# tic_tac_toe.start()


class Label:
    def __init__(self, x, y, w, h, v, s):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.s = s

    def draw(self, img):
        cv2.putText(img, self.v, (self.x + 25, self.y + 40),
                    cv2.FONT_HERSHEY_PLAIN, self.s, (255, 255, 255), self.s)

    def resize(self, w, h, img):
        cv2.putText(img, self.v, (self.x + w, self.y + h),
                    cv2.FONT_HERSHEY_PLAIN, self.s, (255, 255, 255), self.s)

    def color(self, rgb, img):
        cv2.putText(img, self.v, (self.x + 25, self.y + 40),
                    cv2.FONT_HERSHEY_PLAIN, self.s, rgb, self.s)

    def text(self, value, img):
        cv2.putText(img, value, (self.x + 25, self.y + 40),
                    cv2.FONT_HERSHEY_PLAIN, self.s, (255, 255, 255), self.s)

    def shrink(self, value, limit, img):
        cv2.putText(img, (self.v[:limit + 1][-1] + value), (self.x + 25, self.y + 50), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 255, 255), 2)


class Button:

    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def focused(self, img, x, y):
        return self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height

    def click(self, img, value):
        if self.value in ['X', 'O', ' '] and value != self.value:
            self.value = value
            self.text(self.value, img)

    def draw(self, img):
        self.border((255, 255, 255), img)
        self.text(self.value, img)

    def background(self, rgb, img):
        cv2.rectangle(
            img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), rgb, cv2.FILLED)

    def border(self, rgb, img):
        cv2.rectangle(
            img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), rgb, 2)

    def text(self, value, img):
        self.value = value
        cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)




def main():
    pTime = 0
    cTime = 0

    primary_monitor = {}
    for m in get_monitors():
        print("Connected monitors {}".format(m))
        if m.is_primary:
            primary_monitor = m
            break

    cap = cv2.VideoCapture(1) # mobile device = 1
    cap.set(3, primary_monitor.width)
    cap.set(4, primary_monitor.height)
    detector = HandDetector(detectionCon=0.8, maxHands=2)

    # creating Button
    button_values = [[" ", " ", " "],
                     [" ", " ", " "],
                     [" ", " ", " "]]
    button_components = []

    default_width = 700
    default_height = 100

    for x in range(3):
        for y in range(3):
            pos_x = x * 100 + default_width  # starting from 700 pixel in the width
            pos_y = y * 100 + default_height  # starting from 100 pixel in the height
            button_components.append(
                Button((pos_x, pos_y), 100, 100, button_values[x][y]))

    # to store the whole next_player from the calculator
    global next_player
    next_player = " "

    # to avoid duplicated value inside calculator in event writing
    delay_counter = 0
    cell_counter = 3 * 3

    tip_ids = [4, 8, 12, 16, 20]

    sounds = next(walk("media"), (None, None, []))[2]
    for sound in sounds:
        print("Available sounds:")
        print("File: {}".format(sound))

    while cap.isOpened():

        success, img = cap.read()
        img = cv2.flip(img, 1)

        # detection hand
        hand, img = detector.findHands(img, flipType=False)

        for button in button_components:
            button.draw(img)

        if len(hand) == 1:
            landmarks = hand[0]["lmList"]
            distance, _, img = detector.findDistance(
                landmarks[8][:2], landmarks[12][:2], img)
            x, y = landmarks[8][:2]

            if len(landmarks) != 0 and distance < 65:

                for button in button_components:
                    if button.focused(img, x, y) and delay_counter == 0:
                        button.click(img, next_player)
                        cell_counter -= won(img, next_player, button.value)
                        delay_counter = 1

                # Tested but too fast
                # sound = pyglet.resource.media("media/" + sounds[sound_index - 1], streaming=False)
                # sound.play()

        # avoid duplicates
        if delay_counter != 0:
            delay_counter += 1
            # i did not add value into display calculator
            # after passing 10 frames
            if delay_counter > 10:
                delay_counter = 0

        cv2.imshow("Image", img)

        key = cv2.waitKey(1)
        if key == ord('q'):  # to stop the program
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
