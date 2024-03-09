import pygame
"""
Module: Player.py

This module contains classes for managing the Player.

Classes:
    - FoodDisplay: Represents the icon the player holds up on selection.
    - Player: Represents the player character.
"""

class FoodDisplay(pygame.sprite.Sprite):
    """
    Class representing the icon the player holds up on selection.

    Attributes:
        image (Surface): The sprite of the object.
        rect (Rect): The rectangular area around the image.
        timeSpawned (int): The time the object was spwaned.
    """

    def __init__(self, x, y, image):
        """
        Initialize the FoodDisplay object.

        Args:
            x (int): The x coordinate of the image.
            y (int): The x coordinate of the image.
            image (str): The file path of sprite.
        """
        pygame.sprite.Sprite.__init__(self) # initialize base class
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.timeSpawned = pygame.time.get_ticks()

        self.rect.center = [x, y] # centers the image on the x and y coords

    def update(self):
        """
        Despawns the FoodDisplay object after 600ms has elapsed.
        """
        if (pygame.time.get_ticks() - self.timeSpawned > 600):
            self.kill()


class Player(pygame.sprite.Sprite):
    """
    Class representing the player character.

    Attributes:
        image (Surface): The sprite of the object.
        rect (Rect): The rectangular area around the image.
        timeSpawned (int): The time the object was spwaned.
        score (int): The player score.
        moveSpeed (int): The amount pixels to move with each button press.
        selectActionCooldown (int): The amount of ms to freeze the player for after they hit space.
        lastSelected (int): The timestamp of when user hit space.
        selectedFood (str): File path of selected food
    """

    def __init__(self, x, y):
        """
        Initialize the Player object.

        Args:
            x (int): The x coordinate of the image.
            y (int): The x coordinate of the image.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/player.png") # load sprite
        self.rect = self.image.get_rect()
        self.score = 0
        self.moveSpeed = 300      
        self.selectActionCooldown = 600
        self.lastSelected = pygame.time.get_ticks()
        self.selectedFood = "sprites/food1.png"

        self.rect.center = [x, y] # center rectangle on x and y parameters
    
    def getPosition(self):
        """
        Returns player x position.
        """
        return self.rect.centerx
    
    def getScore(self):
        """
        Returns player score.
        """
        return self.score
    
    def reset(self):
        """
        Resets player score to 0.
        """
        self.score = 0

    def setSelectedFood(self, food):
        """
        Sets selectedFood to food.

        Args:
           food (str): The filepath of the food sprtie.
        """
        self.selectedFood = food

    def move(self, keyPressed):
        """
        Moves the player depending on the key pressed.

        Args:
           keyPressed (keyPressed): The key the user has hit.
        """
        if keyPressed[pygame.K_a] and self.rect.left > 490: # if the user hits 'a' and is not at the boundary
            self.rect.x -= self.moveSpeed
        elif keyPressed[pygame.K_d] and self.rect.right < 790: # if the user hits 'd' and is not at the boundary
            self.rect.x += self.moveSpeed

    def select(self, currentTime, foodGroup, customer):
        """
        Returns True or False if user matched the food with customer order.

        Args:
           currentTime (int): The current timestamp.
           foodGroup (SpriteGroup): The sprite group for FoodDisplay objects.
           customer (Customer): The customer to compare order.
        """
        self.image = pygame.image.load("sprites/player1.png") # load select sprite
        food = FoodDisplay(self.rect.left, self.rect.centery, self.selectedFood) # create food display
        foodGroup.add(food) # add food to sprite group for drawing
        self.lastSelected = currentTime # put user on cooldown
        if self.selectedFood == customer.order: # Check if user made the right choice
            self.score += 100
            return True
        else:
            return False

    def update(self, foodGroup, customer):
        """
        Returns True or False if user matched the food with customer order. Gets called every frame

        Args:
           foodGroup (SpriteGroup): The sprite group for FoodDisplay objects, to be passed to select function.
           customer (Customer): The customer to compare order, to be passed to select function.
        """
        keyPressed = pygame.key.get_pressed() # key the user pressed
        currentTime = pygame.time.get_ticks() # timestamp of function call

        if currentTime - self.lastSelected > self.selectActionCooldown: # if the user is not on cooldown
            self.image = pygame.image.load("sprites/player.png") # load regular sprite
            self.move(keyPressed) # player move
            if keyPressed[pygame.K_SPACE]: # player selection
                return self.select(currentTime, foodGroup, customer)