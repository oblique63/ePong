#!/usr/bin/python
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

#----{ Ball Class }---------------------------------------------------------------------------------------------------------------------------------------
class Ball():
    def __init__(self, x, y, speed=7, size=8):
        self.size = size
        self.speed = speed
        self.x = x
        self.y = y
        self.movement = {"x":"right","y":"up"} # x: "left", "right"; y: ""=no movement, "up", "down"
        self.rect_area = ((self.x,self.y),(self.size,self.size))
        self.rect = pygame.draw.rect(background, (225,225,225),self.rect_area, 0)
        
    def collide(self, y_direction="", x_direction="right"):
        self.movement["x"] = x_direction
        if y_direction:
            self.movement["y"] = y_direction
        
    def move(self):
        "Move the ball according to the direction it is going"
        if self.movement["x"] is "right":
            self.x += self.speed
        else:
            self.x -= self.speed
        if self.movement["y"] is "up":
            self.y += self.speed
        elif self.movement["y"] is "down":
            self.y -= self.speed
        self.rect_area = ((self.x,self.y),(self.size,self.size))
        self.rect = pygame.draw.rect(background, (225,225,225),self.rect_area, 0)
            
    def update(self, x_edge, y_edge):
        "Determines ball movement and location, then moves ball. Returns new score"
        # Check if ball is within the bounds of the X-axis, and redirect it if it is not
        if self.x >= x_edge:
            self.movement["x"] = "left"
        elif self.x <= 0:
            # If it's on the left edge of the screen, deduct a point
            self.movement["x"] = "right"
            self.move()
            return -1
        
        # Check if ball is within the bounds of the Y-axis, and redirect it if it is not
        if self.y >= y_edge:
            self.movement["y"] = "down"
        elif self.y <= 0:
            self.movement["y"] = "up"

        # Move the ball
        self.move()
        return 0

#----{ Paddle Class }-----------------------------------------------------------------------------------------------------------------------------------
class Paddle():
    def __init__(self, position, indent=7, speed=23, height=40, width=8):
        self.height = height
        self.width = width
        self.speed = speed
        self.indent = indent
        self.position = position
        self.rect_area = ((self.indent, self.position),(self.width, self.height))
        self.rect = pygame.draw.rect(background, (225,225,225),self.rect_area, 0)
    def update(self):
        self.rect_area = ((self.indent, self.position),(self.width, self.height))
        self.rect = pygame.draw.rect(background, (225,225,225),self.rect_area, 0)
       

#----{ Initialize Objects }---------------------------------------------------------------------------------------------------------------------------------       
x = 460
y = 300
screen = pygame.display.set_mode((x+5, y+5))
pygame.display.set_caption("ePong")
    
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

paddle1 = Paddle(y/2)

ball = Ball(paddle1.width+paddle1.indent-2, paddle1.position)
ball2 = Ball(paddle1.width+paddle1.indent-2, paddle1.position)

middle_line = (((x+5)/2,0),(5,y+5))

score = 0
high_score = 0
font = pygame.font.Font(pygame.font.get_default_font(), 17)
score_text = font.render("Score: "+str(score), False, (225,225,225))
high_score_text = font.render("High Score: "+str(high_score), False, (180,180,180))


#----{ Game Loop }---------------------------------------------------------------------------------------------------------------------------------------------
clock = pygame.time.Clock()
keepGoing = True
while keepGoing:
    clock.tick(30)
    background.fill((0, 0, 0))
    
    pygame.draw.rect(background, (155,155,155),middle_line, 0)

    paddle1.update()
    score += ball.update(x,y)
    
    if score >= 10:
        score += ball2.update(x,y)

    if not pygame.event.peek(KEYDOWN) and paddle1.rect.colliderect(ball.rect):
        ball.collide()
        score += 1
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if paddle1.position < y-paddle1.height:
                        paddle1.position += paddle1.speed
                    if paddle1.rect.colliderect(ball.rect):
                        ball.collide("down")
                        score += 1
                    elif score >= 10 and paddle1.rect.colliderect(ball2.rect):
                        ball2.collide("down")
                        score += 1
                        
			        
                elif event.key == K_UP:
                    if paddle1.position > 0:
                        paddle1.position -= paddle1.speed
                    if paddle1.rect.colliderect(ball.rect):
                        ball.collide("up")
                        score += 1
                    elif score >= 10 and paddle1.rect.colliderect(ball2.rect):
                        ball2.collide("up")
                        score += 1
                       
    if score > high_score:
        high_score = score
    high_score_text = font.render("High Score: "+str(high_score), False, (180,180,180))
    background.blit(high_score_text,(((x+5)/6)*4,7))
    
    score_text = font.render("Score: "+str(score), False, (225,225,225))
    background.blit(score_text,((x+5)/6,7))
    
    screen.blit(background, (0, 0))
    pygame.display.flip()

