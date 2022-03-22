# Day86-Professional Portfolio Project 5 : GUI Breakout Game

from turtle import Screen
from paddle import Paddle
from ball import Ball
from bricks import Bricks
from scoreboard import Scoreboard
# import random
import time

screen = Screen()
screen.screensize(800, 600, "black")
screen.title("Breakout Game")
screen.tracer(0)

paddle = Paddle()
x, y = paddle.pos()
print(f"x: {x}, y: {y}")
ball = Ball((x, y+19))

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

    bricks.ball_collision(ball, scoreboard)

    # game over
    if ball.ycor() < -320:
        print(f"main - distance : {paddle.distance(ball)}")
        print(f"main - ball - {ball.xcor()}, {ball.ycor()}")
        print(f"main - paddle - {paddle.xcor()}, {paddle.ycor()}")

        ball.goto(1000, 1000)

        game_is_on = False
        scoreboard.game_over()
        break

    # level up
    if len(bricks.all_bricks) <= 0:
        # for _ in range(5):
        #     ball.move(paddle)
        if ball.y_move < 0:
            wait_time = int(200 // abs(ball.y_move))
        else:
            wait_time = int(400 // abs(ball.y_move))

        for _ in range(wait_time):
            time.sleep(0.1)
            screen.update()
            ball.move(paddle)

        scoreboard.level_up()
        ball.speed_down()
        paddle.level_up()
        bricks.level_up()

screen.exitonclick()