from turtle import Turtle
import random

COLORS = ["#6495ED", "#B0E0E6", "#00BFFF", "#00FFFF", "#40E0D0", "#5F9EA0", "#7FFFD4", "#3CB371",
          "#00FF7F", "#228B22", "#00FF00", "#9ACD32", "#F0E68C", "#FFFF00", "#FFD700", "#CD853F",
          "#FF8C00", "#B22222", "#FF6347", "#DC143C", "#9932CC", "#9370DB", "#663399", "#FFC0CB",
          "#FA8072", "#FF69B4", "#C71585", "#FF00FF"]
X_LIST = [-280, -170, -60, 50, 160, 270]
Y_LIST = [280, 255, 230, 205, 180, 155, 130]
# BRICK_COUNT = 10

class Bricks:

    def __init__(self):
        self.all_bricks = []
        self.game_level = 1

    def create_bricks(self):
        for i in X_LIST:
            for j in Y_LIST:
                random_count = random.randint(1, 10)
                if random_count > 7 - self.game_level:
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

                if scoreboard.score % 5 == 0:
                    ball.speed_up()

    def break_brick(self):
        pass

    def level_up(self):
        self.game_level += 1
        self.create_bricks()