import turtle
import time
import os
 
class Object(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(1)
        self.penup()
        self.goto(startx,starty)
        self.color(color)
        self.state ="stop"
 
    def move_right(self):
        self.state = "right"
        self.move()
 
    def move_left(self):
        self.state = "left"
        self.move()
 
    def move(self):
        if self.state == "left":
            self.setheading(180)
            self.forward(5)
            self.state = "stop"
        if self.state == "right":
            self.setheading(0)
            self.forward(5)
            self.state = "stop"
 
ball = Object("circle", "red", 0, -300)
 
def print_stuff():
    ball.setheading(180)
    ball.forward(5)


turtle.onkey(ball.move_right, "d")
turtle.onkey(ball.move_left, "a")
turtle.onkey(print_stuff, "e")
turtle.listen()

 
delay = input("Press enter to finish. > ")