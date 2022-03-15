from turtle import Turtle

ALIGN, FONT = "center", ("Courier", 30, "normal")
POSITION = (220, -300)

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.hideturtle()
        self.color("red")
        self.goto(POSITION)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(f"score: {self.score}", align=ALIGN, font=FONT)

    def increase_score(self):
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGN, font=FONT)
