from turtle import Turtle

TOP, BOTTOM, LEFT, RIGHT = 313, -270, -339, 327

class Ball(Turtle):

    def __init__(self, position):
        super().__init__()
        self.starting_position = position
        self.shape("circle")
        self.goto(position)
        self.color("white")
        # self.turtlesize(0.8, 0.8)
        self.x_move = 8
        self.y_move = 10
        self.speed_up()

        self.penup()

    def move(self, paddle):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        # bounce = False

        # collision with paddle (1)
        # if ball speed is too fast, change the ball to attach the paddle
        if ((BOTTOM + 5 <= self.ycor() <= BOTTOM + 20) and (paddle.xcor() - 40 < self.xcor() < paddle.xcor() + 40) and self.y_move < 0):
            self.goto(new_x, new_y)
            self.bounce_y()

        # collision with paddle (2)
        elif (new_y < paddle.ycor() - 20 < self.ycor() and self.distance(paddle) < 60 and self.y_move < 0) \
            and (self.distance(paddle) < 30 and self.y_move < 0):
            # or ((BOTTOM - 10 <= self.ycor() <= BOTTOM) and (paddle.xcor() - 60 < self.xcor() < paddle.xcor() + 60) and self.y_move < 0):
            # or (self.distance(paddle) < 50 and self.y_move < -15):
                print("paddle-ball")
                print(f"before - x : {self.xcor()}, y : {self.ycor()}")

                new_x = int(self.xcor() * (paddle.ycor()+20) / self.ycor())
                self.goto(new_x, paddle.ycor()+20)
                print(f"after - x : {self.xcor()}, y : {self.ycor()}")

                self.bounce_y()

        # bounce on left wall
        elif new_x <= LEFT <= self.xcor() and self.x_move < 0:
            # print("left wall - before x : ", self.xcor())
            self.goto(LEFT, new_y)
            # print("left wall - after x : ", self.xcor())
            self.bounce_x()

        # bounce on right wall
        elif self.xcor() <= RIGHT <= new_x and self.x_move > 0:
            # print("right wall - before x : ", self.xcor())
            self.goto(RIGHT, new_y)
            # print("right wall - after x : ", self.xcor())
            self.bounce_x()

        # bounce on the ceiling
        elif self.ycor() <= TOP <= new_y and self.y_move > 0:
            self.goto(new_x, TOP)
            self.bounce_y()

        else:
            self.goto(new_x, new_y)

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1

    def reset_position(self):
        self.goto(self.starting_position)
        self.bounce_y()

    def speed_up(self):
        speedup = 1.2
        self.x_move = min(int(self.x_move * speedup), 20)
        self.y_move = min(int(self.y_move * speedup), 24)
        print(f"speed : x_move - {self.x_move}, y_move - {self.y_move}")

    def speed_down(self):
        speeddown = 0.8
        self.x_move = int(self.x_move * speeddown)
        self.y_move = int(self.y_move * speeddown)
