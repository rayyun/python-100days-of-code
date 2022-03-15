from turtle import Turtle

TOP, BOTTOM, LEFT, RIGHT = 313, -240, -339, 327
# TOP, BOTTOM, LEFT, RIGHT = 313, -320, -339, 327
# TOP, BOTTOM, LEFT, RIGHT = 200, -200, -250, 240

class Ball(Turtle):

    def __init__(self, position):
        super().__init__()
        self.starting_position = position
        self.shape("circle")
        self.goto(position)
        self.color("white")
        # self.turtlesize(0.8, 0.8)
        self.speed("slowest")
        self.x_move = 8
        self.y_move = 10
        self.penup()

    def move(self, paddle):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move

        self.goto(new_x, new_y)

        if self.xcor() < LEFT or self.xcor() > RIGHT:
            self.bounce_x()

        if self.ycor() > TOP:
            self.bounce_y()

        if (BOTTOM - 10 <= self.ycor() <= BOTTOM) and (paddle.xcor() - 60 < self.xcor() < paddle.xcor() + 60) and self.y_move < 0:
            self.bounce_y()

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1

    def reset_position(self):
        self.goto(self.starting_position)
        self.bounce_y()