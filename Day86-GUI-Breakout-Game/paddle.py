from turtle import Turtle

PADDLE_SIZE = 6
STARTING_POINT = (0, -250)
LEFT, RIGHT = -300, 290


class Paddle(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.speed("fastest")
        self.turtlesize(1, 5)
        self.color("blue")
        self.goto(STARTING_POINT)

    def go_left(self):
        if LEFT < self.xcor():
            self.goto(self.xcor() - 20, self.ycor())

    def go_right(self):
        if self.xcor() < RIGHT:
            self.goto(self.xcor() + 20, self.ycor())