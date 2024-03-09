import pygame
"""
Module: Timer.py

This module contains the class for managing the game timer.
"""
class Timer:
    """
    Class representing the game timer.

    Attributes:
        initialDuration (int): Initial duration of the timer.
        duration (int): Duration of the timer.
        lastTick (int): Record the time of the last tick.
        font (Font): Font for displaying text
    """

    def __init__(self, duration):
        """
        Initialize the Timer object.

        Args:
            duration (int): Duration of the timer.
        """
        self.initialDuration = duration
        self.duration = duration
        self.lastTick = pygame.time.get_ticks()
        pygame.font.init() # Initialize pygame font module
        self.font = pygame.font.Font(None, 50) # (fontName, size)

    def update(self):
        """
        Update the time on the timer. This gets called every frame.
        """
        currentTime = pygame.time.get_ticks() # get current time
        if currentTime - self.lastTick >= 1000:  # Check if one second has passed
            self.duration -= 1 # decrement timer
            if self.duration < 0: # prevent duration from going less than 0
                self.duration = 0
            self.lastTick = currentTime  # update the last tick time

    def reset(self):
        """
        Reset timer to initalDuration
        """
        self.duration = self.initialDuration
        self.lastTick = pygame.time.get_ticks()

    def draw(self, screen):
        """
        Draws the timer to the screen. This gets called every frame.

        Args:
            screen (Surface): The screen to draw to.
        """
        text = self.font.render(f"Time: {self.duration}", True, (0, 0, 0)) # function to render text (message, antialias, color)
        screen.blit(text, (10, 10)) # function draw the text to screen (text, coords)

    def timesUp(self):
        """
        Returns True if timer duration is 0.
        """
        return self.duration == 0
    