import pygame
"""
Module: SatisfactionBar.py

This module contains the class for managing the overall customer satisfaciton bar at the top of the screen.
"""

class SatisfactionBar(pygame.sprite.Sprite):
    """
    Class representing the overall customer satisfaciton bar.

    Attributes:
        initialValue (int): The initial value of the bar.
        satisfactionValue (int): The current value of the bar.
        decayValue (int): How much the bar will decay by each frame.
    """

    def __init__(self, initialValue, decayValue):
        """
        Initialize the SatisfactionBar object.

        Args:
            initialValue (int): The initial value of the bar.
            decayValue (int): How much the bar will decay by each frame.
        """
        pygame.sprite.Sprite.__init__(self) # initialize base class
        self.initialValue = initialValue
        self.satisfactionValue = initialValue 
        self.decayValue = decayValue

    def update(self):
        """
        Updates the satisfactionValue by the decayValue. This gets called every frame.
        """
        self.satisfactionValue -= self.decayValue


    def updateBar(self, value):
        """
        Updates the satisfactionValue by value.

        Args:
            value (int): The value to update satisfactionValue by.
        """
        self.satisfactionValue += value


    def getSatisfactionValue(self):
        """
        Return the satisfaciton value.
        """
        return self.satisfactionValue

    def reset(self):
        """
        Set satisfactionValue back to the initialValue.
        """
        self.satisfactionValue = self.initialValue

    def draw(self, screen):
        """
        Draws the bar to the screen. This gets called frame.

        Args:
            screen (Surface): The screen to draw to.
        """
        # screen, color, x, y, width, height
        pygame.draw.rect(screen, (251, 180, 200), (300, 10, (self.satisfactionValue), 30))