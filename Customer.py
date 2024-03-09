import pygame
import random
"""
Module: Customer.py

This module contains the class for managing the customers of the cafe.
"""

class Customer(pygame.sprite.Sprite):
    """
    Class representing the customers of the cafe.

    Attributes:
        image (Surface): 1 of 3 random customer sprites.
        rect (Rect): The rectangular area around the image.
        order (str): File path of 1 of 3 possible foods.
        showOrder (bool): Flag determining whether or not to show customer order.
    """

    def __init__(self, x, y):
        """
        Initialize the Customer object.

        Args:
            x (int): The x coordinate of the image.
            y (int): The x coordinate of the image.
        """
        pygame.sprite.Sprite.__init__(self) # initialize base class
        self.image = pygame.image.load("sprites/cat" + str(random.randint(1, 3)) + ".png")
        self.rect = self.image.get_rect()
        self.order = "sprites/food" + str(random.randint(1, 2)) + ".png"
        self.showOrder = False

        self.rect.center = [x, y] # centers the image on the x and y coords

    def delete(self):
        """
        Delete the Customer object.
        """
        self.kill()

    def update(self, screen):
        """
        Updates the Customer object. Show the customer order if the showOrder flag is true. This gets called every frame.

        Args:
            screen (Surface): The screen to draw to.
        """
        if self.showOrder == True:
            screen.blit(pygame.image.load("sprites/bubble.png"), (self.rect.left - 175, self.rect.top - 150)) # loads the order sprite next to the customer
            screen.blit(pygame.image.load(self.order), (self.rect.left - 145, self.rect.top - 115))

    def move(self):
        """
        Moves the Customer object a set distance in line.
        """
        self.rect.y += 75
        self.rect.x -= 150

    def setShowOrder(self):
        """
        Sets showOrder flag to True
        """
        self.showOrder = True
    