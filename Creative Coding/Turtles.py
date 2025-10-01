from turtle import *
def draw_triangle(turtle, xpos, ypos, width, color, heading):
    turtle.penup()
    turtle.goto(xpos, ypos)
    turtle.setheading(heading)
    turtle.pendown()
    turtle.color(color)
    turtle.begin_fill()
    for side in range(3):
        turtle.forward(width)
        turtle.left(120)
    turtle.end_fill()

space = Screen()
alex = Turtle()
draw_triangle(alex, -120, 30, 60, 'green', 60)
draw_triangle(alex, -120, 30, 60, 'green', 240)