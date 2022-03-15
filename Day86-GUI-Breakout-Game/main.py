# Day86-Professional Portfolio Project 5 : GUI Breakout Game

from turtle import Screen
from paddle import Paddle
from ball import Ball
from bricks import Bricks
from scoreboard import Scoreboard
import random
import time

screen = Screen()
screen.screensize(800, 600, "black")
screen.title("Breakout Game")
screen.tracer(0)

paddle = Paddle()
x, y = paddle.pos()
print("x: {x}, y: {y}")
ball = Ball((x, y+19))
# angle = random.randint(100, 145)

bricks = Bricks()
bricks.create_bricks()

scoreboard = Scoreboard()
scoreboard.update_scoreboard()

screen.listen()
screen.onkeypress(paddle.go_left, "Left")
screen.onkeypress(paddle.go_right, "Right")


game_on = True

while game_on:
    time.sleep(0.1)
    screen.update()
    ball.move(paddle)

    # if ball.xcor
    bricks.ball_collision(ball, scoreboard)

    if len(bricks.all_bricks) < 0 or ball.ycor() < -300:
        ball.goto(1000, 1000)
        game_is_on = False
        scoreboard.game_over()


screen.exitonclick()