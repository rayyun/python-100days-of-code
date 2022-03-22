from turtle import Turtle

ALIGN, FONT = "center", ("Courier", 30, "normal")
POSITION = (220, -250)

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.hideturtle()
        self.color("#FF4500")
        self.game_level = 1

        self.goto(POSITION)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"level {self.game_level}\nscore: {self.score}", align=ALIGN, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGN, font=FONT)

    def level_up(self):
        self.game_level += 1
        self.update_scoreboard()