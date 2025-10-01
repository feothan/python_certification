from turtle import *


def tree(turtle, x, y, size, color):
    turtle.color(color)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.setheading(90)
    turtle.forward(100 * size)
    turtle.right(30)
    for i in range(8):
        turtle.forward(25 * size)
        turtle.left(15)
        turtle.forward(25 * size)
        turtle.left(45)
        turtle.forward(50 * size)
        turtle.left(75)
    turtle.setheading(180)
    turtle.penup()
    turtle.forward(25 * size)
    turtle.left(90)
    turtle.pendown()
    turtle.forward(100 * size)


def moon(turtle, x, y, size, color):
    turtle.color(color)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.setheading(25)
    for i in range(16):
        turtle.forward(20 * size)
        turtle.left(10)
    turtle.left(150)
    for i in range(14):
        turtle.forward(20 * size)
        turtle.right(10)


def cloud(turtle, x, y, size, color):
    turtle.color(color)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.setheading(270)
    amount = 1
    for j in range(5):
        for i in range(14):
            amount += .5
            turtle.forward(amount * size)
            turtle.left(15)
        turtle.right(70)


here = Screen()
here.bgcolor("black")
gerald = Turtle()
gerald.speed(0)
moon1 = moon(gerald, -50, 10, .85, "yellow")
cloud1 = cloud(gerald, -140, 75, .5, "white")
cloud2 = cloud(gerald, 140, 80, .7, "white")
tree1 = tree(gerald, 125, -245, 1.3, "green")
tree2 = tree(gerald, 75, -245, 1.1, "brown")
tree3 = tree(gerald, -50, -270, 1.5, "orange")
tree4 = tree(gerald, 0, -245, .9, "pink")