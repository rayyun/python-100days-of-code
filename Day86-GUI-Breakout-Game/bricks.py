from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "gray"]
X_LIST = [-280, -170, -60, 50, 160, 270]
Y_LIST = [280, 255, 230, 205, 180]
# X_LIST = [-340, -230, -120, -10, 100, 210, 320]
# Y_LIST = [280, 255, 230, 205, 180]

class Bricks:

    def __init__(self):
        self.all_bricks = []

    def create_bricks(self):
        for i in X_LIST:
            for j in Y_LIST:
                new_brick = Turtle("square")
                new_brick.turtlesize(1, 5)
                new_brick.penup()
                new_brick.color(random.choice(COLORS))
                new_brick.goto(i, j)
                self.all_bricks.append(new_brick)

    def ball_collision(self, ball, scoreboard):
        for brick in self.all_bricks:
            if (brick.ycor() - 20 <= ball.ycor() <= brick.ycor() + 20) and (brick.xcor() - 60 < ball.xcor() < brick.xcor() + 60):
                brick.goto(1000, 1000)
                ball.bounce_y()
                self.all_bricks.remove(brick)
                scoreboard.increase_score()

    def break_brick(self):
        pass
