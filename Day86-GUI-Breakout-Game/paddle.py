from turtle import Turtle
import random

PADDLE_SIZE = 6
# STARTING_POINT = (0, -250)
STARTING_POINT = (random.randint(-200, 200), -290)
LEFT, RIGHT = -290, 280


class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.speed("fastest")
        self.turtlesize(1, 5)
        self.color("#778899")
        self.goto(STARTING_POINT)
        self.game_level = 1
        self.move_speed = 20

    def go_left(self):
        if LEFT < self.xcor() and LEFT < (self.xcor() - self.move_speed):
            self.goto(self.xcor() - self.move_speed, self.ycor())
        else:
            self.goto(LEFT - 10, self.ycor())

    def go_right(self):
        if self.xcor() < RIGHT and (self.xcor() + self.move_speed) < RIGHT:
            self.goto(self.xcor() + self.move_speed, self.ycor())
        else:
            self.goto(RIGHT + 10, self.ycor())

    def level_up(self):
        self.game_level += 1
        self.move_speed += 20
