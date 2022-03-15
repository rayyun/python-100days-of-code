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


    # def bounce(self, angle):
    #     self.setheading(angle)
    #     # new_angle = angle
    #
    #     while BOTTOM < self.ycor() < TOP:
    #     # while LEFT < self.xcor() < RIGHT:
    #     # while LEFT < self.xcor() < RIGHT and BOTTOM < self.ycor() < TOP:
    #
    #         while (LEFT < self.xcor()) and (self.xcor() < RIGHT) and (BOTTOM < self.ycor()) and (self.ycor() < TOP):
    #             self.forward(10)
    #             # print(f"while-while : {self.xcor()}, {self.ycor()}")
    #
    #
    #         # if self.xcor() >= RIGHT and (BOTTOM < self.ycor() < TOP):
    #         #     print(f"if : {self.xcor()}, {self.ycor()}")
    #
    #             # self.setheading((90 * (angle // 45) - angle) % 360)
    #             # print(f"new angle : {(90 * (angle // 45) - angle) % 360}")
    #
    #             # self.setheading(90 + angle)
    #             # self.setheading(360 - angle)
    #             # self.setheading((180 + angle) % 360)
    #
    #             # self.setheading(angle)
    #         #     self.forward(10)
    #         #     # continue
    #         #
    #         # elif self.xcor() <= LEFT and (BOTTOM < self.ycor() < TOP):
    #         #     print(f"elif - 1st : {self.xcor()}, {self.ycor()}")
    #
    #         if (self.xcor() <= LEFT and 90 <= self.heading() <= 270) or (RIGHT <= self.xcor() and not 90 <= self.heading() <= 270):
    #             self.left(180 - 2 * self.heading())
    #         elif (self.ycor() <= BOTTOM and self.heading() >= 180) or (TOP <= self.ycor() and self.heading() <= 180):
    #             self.left(-2 * self.heading())
    #
    #         # if not (LEFT <= self.xcor() <= RIGHT):
    #         #     self.setheading(180 - 2 * angle)
    #         #
    #         # elif not (BOTTOM <= self.ycor() <= TOP):
    #         #     self.setheading(-2 * angle)
    #
    #         elif self.ycor() >= TOP:
    #                 print(f"elif - 2nd : {self.xcor()}, {self.ycor()}")
    #                 self.setheading(360 - angle)
    #                 self.forward(10)
    #                 continue
    #         elif self.ycor() <= BOTTOM:
    #             print(f"elif - 3rd : {self.xcor()}, {self.ycor()}")
    #             self.forward(0)
    #             self.game_over()
    #             break
    #         else:
    #             break
    #
    #
    #         self.forward(10)
    #
    #
    #
    #
    #
    #
    #             # print(f"elif - 1st : {self.xcor()}, {self.ycor()}")
    #             # # self.setheading((180 + angle) % 360)
    #             # new_angle += 180
    #             # self.setheading(new_angle)
    #             # # self.setheading(180 + angle)
    #             #
    #             #
    #             # # self.setheading(angle)
    #             # self.forward(10)
    #             # # continue
    #             #
    #
    #
    #
    #     # self.forward(0)
    #
    #     # if self.ycor() <= BOTTOM:
    #     #     self.game_over()
    #
    # def game_over(self):
    #     # self.forward(0)
    #     print("Game over!!!")
    #
    #
    # # def bounce(self, angle):
    # #     self.setheading(angle)
    # #     while LEFT < self.xcor() < RIGHT and BOTTOM < self.ycor() < TOP:
    # #         print(f"LEFT : {LEFT}, RIGHT : {RIGHT}, BOTTOM : {BOTTOM}, TOP : {TOP} --> x: {self.xcor()} / y: {self.ycor()}")
    # #
    # #         if self.xcor() < LEFT or self.xcor() > RIGHT or self.ycor() < BOTTOM or self.ycor() > TOP:
    # #             break
    # #         self.forward(10)
    # #         # print(self.pos())
    # #     else:
    # #         self.forward(0)
    # #         print(f"stop - {self.pos()}")
    # #
    # #         # self.setheading(360 - angle)
    # #         # self.forward(10)
    # #         # continue
    # #
    # #     self.forward(0)
