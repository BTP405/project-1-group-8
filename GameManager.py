import pygame
from pymongo import MongoClient

from Timer import Timer
from SatisfactionBar import SatisfactionBar
from Customer import Customer
from Player import Player

"""
Module: GameManager.py

This module contains the class for managing the entire game.
"""

class GameManager():
    """
    Class handles the flow and menu of the game.

    Attributes:
        screenWidth (int): The width of the screen.
        screenHeight (int): The height of the screen.
        screen (Surface): The screen to display everything on.
        fpsManager (Clock): Manages the frame rate of the game.
        gamePaused (bool): Determines if the game is paused.
        lose (bool): Determines if the user has lost.
        gameTimer (Timer): Represents the game timer
        satisfactionBar (SatisfactionBar): Represents the satisfaction bar
        playerGroup (SpriteGroup): The sprite group for Player object.
        foodGroup (SpriteGroup): The sprite group for FoodDisplay objects.
        cusGroup (SpriteGroup): The sprite group for Customer objects.
        uri (str): Connection uri.
        client (MongoClient): The mongo client.
    """

    def __init__(self):
        """
        Initialize the GameManager object.
        """
        self.screenWidth = 1280
        self.screenHeight = 720
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Sugar Pawradise')
        self.fpsManager = pygame.time.Clock()

        self.gamePaused = False
        self.lose = False
        self.gameTimer = Timer(30)
        self.customerBar = SatisfactionBar(100, 0.2)

        self.playerGroup = pygame.sprite.Group(Player(self.screenWidth // 2 - 150, self.screenHeight // 2 + 200))
        self.foodGroup = pygame.sprite.Group()
        self.cusGroup = pygame.sprite.Group()

        self.uri = "mongodb+srv://javier:O3bnYO9Cx0GUzMEO@cluster0.xlzcpze.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(self.uri) # Create a new client and connect to the server

    def spawnCustomers(self):
        """
        Spawns in customers objects.
        """
        for i in range(3):
            self.cusGroup.add(Customer(350 + i*150, 300 + -i*75)) # spawn 3 staggered customers 

    def startGame(self):
        """
        Handles gameplay loop.
        """
        while True:
            self.fpsManager.tick(60) # set game to 60fps

            # draw sprites to screen
            self.screen.blit(pygame.image.load("sprites/bg.jpg"), (0, 0))
            self.cusGroup.draw(self.screen)
            self.screen.blit(pygame.image.load("sprites/food1.png"), (315, 365))
            self.screen.blit(pygame.image.load("sprites/food2.png"), (615, 365))
            self.gameTimer.draw(self.screen)
            self.customerBar.draw(self.screen)
            self.playerGroup.draw(self.screen)
            self.foodGroup.draw(self.screen)

            if self.gamePaused: # if paused naviagte to pause menu
                self.pauseMenu()
                self.gamePaused = False
            else:
                if not self.gameTimer.timesUp() and not self.lose: # run game if time isn't up or player hasn't lost
                    if(len(self.cusGroup.sprites()) < 1): # spawn more customers when there are less than 1 left
                        self.spawnCustomers()
                    self.cusGroup.sprites()[0].setShowOrder() # show order of first customer

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: # if player hits x in top right, close game
                            pygame.quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE: # if player hits ESC, pause game
                                self.gamePaused = True
                            else:
                                # determine player selected food with position
                                playerPos = self.playerGroup.sprites()[0].getPosition()
                                if playerPos > self.screenWidth//2:
                                    selectedFood = "sprites/food2.png"
                                else:
                                    selectedFood = "sprites/food1.png"
                                self.playerGroup.sprites()[0].setSelectedFood(selectedFood)
                        
                                # check if player matched the order, update customerBar
                                selectResult = self.playerGroup.sprites()[0].update(self.foodGroup, self.cusGroup.sprites()[0])
                                if selectResult == False:
                                    self.customerBar.updateBar(-20)
                                elif selectResult == True:
                                    self.cusGroup.sprites()[0].delete()
                                    self.customerBar.updateBar(20)
                                    for customer in self.cusGroup.sprites(): # move customers up in line if successful
                                        customer.move()

                    # run the update function for all groups
                    self.foodGroup.update()
                    self.cusGroup.update(self.screen)
                    self.customerBar.update()
                    self.gameTimer.update()

                    # if customerBar hits 0, lose game
                    if self.customerBar.getSatisfactionValue() < 0:
                        self.lose = True

                # if timer runs out, end game
                else:
                    if self.gameTimer.timesUp():
                        self.endScreen("Times Up!")
                    else:
                        self.endScreen("You Lose!")
                    
            for event in pygame.event.get(): # if player hits x in top right outside of gameloop, close game
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()

    def mainMenu(self):
        """
        Displays the main menu and gets inputs.
        """
        while True:
            self.screen.blit(pygame.image.load("sprites/mainMenu.jpg"), (0, 0))

            for event in pygame.event.get(): # find key user pressed and execute function
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.startGame()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                    elif event.key == pygame.K_e:
                        self.leaderBoard()

            pygame.display.update()
    
    def pauseMenu(self):
        """
        Displays the pause menu and gets inputs.
        """
        while True:
            self.screen.blit(pygame.image.load("sprites/pause.jpg"), (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                    elif event.key == pygame.K_e:
                        self.mainMenu()

            pygame.display.update()

    
    def endScreen(self, message):
        """
        Displays the end screen and gets inputs.

        Args:
            message (str): The end message to print.
        """
        playerName = ""
        scoreSaved = False
        while True:
            self.screen.blit(pygame.image.load("sprites/end.jpg"), (0, 0))
            font = pygame.font.Font(None, 48)
            text = font.render(f"{message} your score is {self.playerGroup.sprites()[0].getScore()}", True, (208, 113, 148))
            text_rect = text.get_rect()
            text_rect.center = (self.screenWidth // 2, self.screenHeight // 4)
            self.screen.blit(text, text_rect)

            if not scoreSaved:
                input_font = pygame.font.Font(None, 36)
                input_text = input_font.render("Start typing to input your name and press ENTER to save your score:", True, (0, 0, 0))
                input_text_rect = input_text.get_rect()
                input_text_rect.center = (self.screenWidth // 2, self.screenHeight // 2 + 250)
                self.screen.blit(input_text, input_text_rect)
                
                playerNameFont = pygame.font.Font(None, 36)
                playerNameText = playerNameFont.render(playerName, True, (0, 0, 0))
                playerNameRect = playerNameText.get_rect()
                playerNameRect.center = (self.screenWidth // 2, self.screenHeight // 2 + 275)
                self.screen.blit(playerNameText, playerNameRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: # reset game
                        self.lose = False
                        self.gameTimer.reset()
                        self.customerBar.reset()
                        self.playerGroup.sprites()[0].reset()
                        self.startGame()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                    elif event.key == pygame.K_e:
                        self.leaderBoard()
                    elif event.key == pygame.K_RETURN:
                        scoreSaved = True
                        leaderboardData = {"name": playerName, "score": self.playerGroup.sprites()[0].getScore()},
                        db = self.client['gameDatabase']
                        leaderboard = db['leaderboard']
                        leaderboard.insert_many(leaderboardData)
                    elif event.unicode.isalnum() and len(playerName) < 10 and not scoreSaved:
                        playerName += event.unicode
                    elif event.key == pygame.K_BACKSPACE and not scoreSaved:
                        playerName = playerName[:-1]
            pygame.display.update()

        
    def leaderBoard(self):
        """
        Displays the leader board screen and gets inputs.
        """
        while True:
            self.screen.blit(pygame.image.load("sprites/leaderBoard.jpg"), (0, 0))

            db = self.client['gameDatabase']
            leaderboard = db['leaderboard']
            leaderboardData = leaderboard.find().sort("score", -1).limit(5)
            
            count = 0
            for player in leaderboardData:
                font = pygame.font.Font(None, 48)
                text = font.render(f"{count+1}. {player['name']}: {player['score']}", True, (0, 0, 0))
                self.screen.blit(text, (self.screenWidth // 2 - 100, 125 + count*50))
                count += 1

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE: 
                            self.mainMenu()
                            return
                        elif event.key == pygame.K_q:
                            pygame.quit()
            pygame.display.update()