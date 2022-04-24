import pygame, sys
import pygame.locals as gameGlobals
from random import randint
windX = 1920
windY = 1080
window = pygame.display.set_mode((windX,windY))

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
SKYBLUE = (7,187,245)
GREY = (90,90,90)
GREY2 = (44,44,44)
GREY3 = (165,165,165)
GREY4 = (10,10,10)
class player(pygame.sprite.Sprite):
    def __init__(self,xPos,yPos):
        super().__init__()
        #getting sprites
        self.sprites = []#ship sprites
        for x in range(6):
            self.sprites.append(pygame.image.load("slimeShip_%s.png"%(x)).convert_alpha())
        self.spritesCar = []#car sprites
        for x in range(3):
            self.spritesCar.append(pygame.image.load("slimeCar_%s.png"%(x)).convert_alpha())
        #going though animation frames
        self.current_sprite = 0 
        self.image = self.sprites[self.current_sprite]
        self.animate = 1 #animates every x frames
        #postion variables
        self.xPos = xPos
        self.yPos = yPos
        self.playerSpeed = 20 #starting speed for obstacles to move
        #jumping variables
        self.jump = False #in a jump or not
        self.maxheight = 50
        self.minheightNorm = windY-600
        self.minheight = self.minheightNorm
        self.jumpSpeed = 50

        #car vars
        self.carMode = False #car mode when "crouching"

        #rect
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

        #health and money saved by txt file
        try: #tries to open txt file
            self.myFile = open("gameData.txt")
            self.maxHp = self.myFile.readline()
            self.money = self.myFile.readline()
            self.myFile.close()
        except:#creates a new file with defult money and max heatlh
            #creates a file
            self.myFile = open("gameData.txt","x")
            self.myFile.close()
            #writes down max health and money
            self.myFile = open("gameData.txt","w")
            self.myFile.write("1")
            self.myFile.write("\n0")
            self.myFile.close
            #defines the maxhp and money varables
            self.myFile = open("gameData.txt")
            self.maxHp = int(self.myFile.readline())
            self.money = int(self.myFile.readline())
            self.myFile.close()
        self.health = int(float(self.maxHp))

    def fileWrite(self,highScore): #writes in teh gamedata file the max heath and 
        self.myFile = open("gameData.txt","w")
        self.myFile.write(str(int(self.maxHp))) #heath   
        self.myFile.write("\n" + str(int(self.money)))#money
        self.myFile.write("\n" + str(highScore))#score
        self.myFile.close()

    def draw(self): 
        if self.animate == 2: #animates every x frames
            self.animate = 1
            if self.carMode == False: #normal flying mode
                self.current_sprite += 1
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                
                self.image = self.sprites[self.current_sprite]
                self.image = pygame.transform.scale(self.image,(int(self.size[0]/2),int(self.size[1]/2)))

                self.minheight = self.minheightNorm #normal heighnt

            else: #car mode is true
                self.current_sprite += 1
                if self.current_sprite >= len(self.spritesCar):
                    self.current_sprite = 0

                self.image = self.spritesCar[self.current_sprite]
                self.image = pygame.transform.scale(self.image,(int(self.size[0]/2),int(self.size[1]/2.5)))

                self.minheight = (windY - 300)

        else:
            self.animate += 1

    def jumpMove(self): #checks if player is currently jumping
        if self.yPos <= self.minheight and self.jump == False: #when the player is off the ground
            self.yPos += 9.81 *2 #gravity

        if self.yPos <= self.minheight-100 and self.jump == False and self.carMode == True: #when the player is off the ground but in car mode
            self.yPos += 9.81 *14 #gravity

        if self.yPos > self.minheight and self.jump == False and self.carMode == True: #when the car mode is past its targtet
            self.yPos = self.minheight
        if self.yPos > self.minheight and self.carMode == False:#forces the ship to move up if its past the min heigt
            self.yPos -= 9.81 *2


        if self.jump == True:#not currently in a jump
            self.yPos -= self.jumpSpeed
        
        if self.yPos <= self.maxheight:# checks if the player is reaced max height and stops moving forward
            self.jump = False 
        
class explosion(pygame.sprite.Sprite):
        def __init__(self,xPos,yPos,exploded): #type of obstacal chosen by type variable
            super().__init__()   
            #sprites 
            self.sprites = []
            for x in range(8):
                self.sprites.append(pygame.image.load("explosion_ %s.png"%(x)).convert_alpha())
            self.current_sprite = -1
            self.image = self.sprites[self.current_sprite]

            #postions
            self.xPos = xPos
            self.yPos = yPos         
              
            self.exploded = False #if the explosion animation is done or not
            #rect 
            self.rect = self.image.get_rect()

        def draw(self):
            
            if x.current_sprite < 6: 
                self.current_sprite += 1
            self.image = self.sprites[self.current_sprite]  

            if self.current_sprite >= 6: #when the animation is done
                self.exploded = True #explotion is done

class obstacle(pygame.sprite.Sprite): #obstacal class 
    def __init__(self,obType,xPos): #type of obstacal chosen by type variable
        super().__init__()
        #sprite
        self.sprites = []
        for x in range(2):
            self.sprites.append(pygame.image.load("chainSaw_%s.png"%(x)).convert_alpha())
        self.spritesWall = []
        for x in range(2):
            self.spritesWall.append(pygame.image.load("wall_%s.png"%(x)).convert_alpha())
        self.current_sprite = 0 
        self.animate = 1
        self.image = self.sprites[self.current_sprite]  
        #positons and type
        self.obType = obType
        self.xPos = xPos
        self.attackable = True
        if self.obType == 1: #ground obsacle
            self.yPos = randint(450,520) #random height for jumping obscal
        if self.obType == 2: #air obsacle
            self.yPos = -30
        if self.obType == 3:
            self.yPos = 45

        #rectangle
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        #self.rect.topleft = [xPos,yPos]
      
        
    def draw(self):
        if self.animate == 3:#aniamtes every other frame
            self.animate = 1
            if self.obType <= 2: #ob type one or 2
                if self.attackable == True: #animates if the objet is attackable
                    self.current_sprite += 1
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                self.image = self.sprites[self.current_sprite]
                #self.image.fill(WHITE)
                
            elif self.obType == 3: #wall type
                if self.attackable == True:
                    self.current_sprite = 0
                else:
                    self.current_sprite = 1
                self.image = self.spritesWall[self.current_sprite]
        
        else:
            self.animate += 1
        

    def move(self,speed):
        self.xPos -= speed

class coin(pygame.sprite.Sprite):
    def __init__(self,xPos,yPos):
        super().__init__()
        self.sprites = []
        for x in range(13):#coin list
            self.sprites.append(pygame.image.load("coin_%s.png" % x))
        self.current_sprite = 0 
        self.image = self.sprites[self.current_sprite] 
        
        #varables
        self.animateFrame = 0
        self.rect = self.image.get_rect()
        self.xPos = xPos
        self.yPos = yPos
        self.collectable = True #the coin is able to be collected

    def draw(self):
        if self.collectable == True:
            if self.animateFrame == 3:
                self.current_sprite += 1
                self.image = self.sprites[self.current_sprite] 
                self.animateFrame = 0
            else:
                self.animateFrame += 1
            if self.current_sprite >= len(self.sprites)-1:
                self.current_sprite = 0

    def move(self,speed):
        self.xPos -= speed
        
class ambientObj(pygame.sprite.Sprite):
    def __init__(self,objType,xPos):
        super().__init__()
        #sprites
        self.sprites = []
        self.sprites.append(pygame.image.load("steelBeam_0.png").convert_alpha())
        self.current_sprite = 0 
        self.image = self.sprites[self.current_sprite] 

        #variables
        self.objType = objType #differenmt abient objects

        #rectangle
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()

        # pos varablkes
        self.xPos = xPos
        if self.objType == 0: #floor beam
            self.yPos = windY - (self.size[1] -55)
        if self.objType == 1: #roof beam
            self.yPos = -100

    def draw(self): #changes between different ambieant objcects
        if self.objType == 0 or self.objType == 1: #steel beam object roof or floor
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite] 
        

    def move(self,speed):
        self.xPos -= speed

def fileWriteMenu(): #checks how much moeny and hp is in the data file
    myFile = open("gameData.txt")
    maxHp = int(myFile.readline())
    money = int(myFile.readline())
    highScore = int(myFile.readline())
    myFile.close()

    return maxHp,money,highScore
    

def buyHp(cost,money,maxHp,highScore): #adds a heart and removes the cost from the money
    if money-cost >= 0: #if the palyer has enough money to buy hearts
        myFile = open("gameData.txt","w")
        myFile.write(str(maxHp+1)) #heath   
        myFile.write("\n"+ str(money-cost))#money
        myFile.write("\n" + str(highScore))
        myFile.close
    
#innits
pygame.init()
pygame.font.init()
pygame.mixer.init()
#images
heartImg = pygame.image.load("heart_0.png").convert_alpha() #heart image for hud
instructionImg = pygame.image.load("instruction.png").convert_alpha()
enterImg = pygame.image.load("enter.png").convert_alpha()
continueImg = pygame.image.load("continue.png").convert_alpha()

coinList = []
coinListFrame = 0
coinFrameTrue = 1
for x in range(13):#coin list
    coinList.append(pygame.image.load("coin_%s.png" % x))
#fonts
pixelFont = pygame.font.Font("slkscr.ttf",100)
pixelFontSmall = pygame.font.Font("slkscr.ttf",70)
pixelFontLarge = pygame.font.Font("slkscr.ttf",200)
#text
    #menus
start = pixelFont.render(str("START"),False,WHITE) 
exitText = pixelFont.render(str("EXIT"),False,WHITE)
hpUpText = pixelFont.render(str("+1"),False,WHITE)
gameOverText = pixelFontLarge.render(str("GAME OVER"),False,RED)
titleText = pixelFontLarge.render("SLIME RUN",False,(127,255,0))

all_sprites_list = pygame.sprite.Group()
ambient_list = pygame.sprite.Group()
moveSprite = pygame.sprite.Group()
clock = pygame.time.Clock()


#sounds
coinSound = pygame.mixer.Sound('coin.wav')
jumpSound = pygame.mixer.Sound('jump.wav')
explosionSound = pygame.mixer.Sound("explosionSound.wav")
hitSound = pygame.mixer.Sound("hitSound.wav")
deathSound = pygame.mixer.Sound("death_screen.wav")

while True: #main loops
    color1 = GREY2
    color2 = GREY2
    color3 = GREY2
    menuChoice = 1
    menu = True

    while menu: #menu loop
        window.fill(BLACK) #filled in 
        maxHpM,moneyM,highScoreM = fileWriteMenu() #gets money and hp variables
        moneyText = pixelFont.render(str(moneyM),False,WHITE)
        moneyCost = pixelFont.render(str(maxHpM*15),False,WHITE)
        healthText = pixelFont.render("x" + str(maxHpM),False, RED)
        highScoreText = pixelFontSmall.render("HIGH SCORE:" + str(highScoreM),False,WHITE)
        if menuChoice == 1:
            color1 = GREY3
            window.blit(enterImg,(windX/2+290,windY/2-200))
        else:
            color1 = GREY2
        if menuChoice == 2:
            window.blit(enterImg,(windX/2+290,windY/2))
            if maxHpM * 10 > moneyM: #if the cost to buy a heart is more than the money had
                color2 = GREY4
            else:
                color2 = GREY3
        else:
            color2 = GREY2
        if menuChoice == 3:
            window.blit(enterImg,(windX/2+290,windY/2+200))
            color3 = GREY3
        else:
            color3 = GREY2

        pygame.draw.rect(window,color1,(windX/2-250,windY/2-200,500,100))  
        pygame.draw.rect(window,color2,(windX/2-250,windY/2,500,100))
        pygame.draw.rect(window,color3,(windX/2-250,windY/2+200,500,100))  
        #blit menu text
        window.blit(start,(windX/2-150,windY/2-200))
        window.blit(exitText,(windX/2-100,windY/2+200))
        window.blit(hpUpText,(windX/2-250,windY/2))
        window.blit(moneyText,(windX-250,0))
        window.blit(moneyCost,(windX/2,windY/2))
        window.blit(healthText,(0,0))
        window.blit(highScoreText,(windX/2-200,0))
        
        #blit image
        window.blit(heartImg,(windX/2-120,windY/2))
        window.blit(heartImg,(windX/2-120,windY/2))
        window.blit(coinList[coinListFrame],(windX-360,0))
        window.blit(coinList[coinListFrame],(windX//2+125+80,windY/2))
        window.blit(instructionImg,(0,50))
        window.blit(titleText,(450,90))
        

        #blit of heart image
        if maxHpM >= 100:
            window.blit(heartImg,(290,0)) #heat image
        elif maxHpM >= 10:
            window.blit(heartImg,(220,0)) #heart image
        else:
            window.blit(heartImg,(140,0)) #heart image


        if coinFrameTrue == 3:#every other frame animates
            coinListFrame += 1
            coinFrameTrue = 1
        else:
            coinFrameTrue += 1

        if coinListFrame >= len(coinList):
            coinListFrame = 0
        pygame.display.update()#refresh all draws
        clock.tick(60)

        for event in pygame.event.get():# quits with esc
            if event.type == pygame.KEYDOWN:
                #scrolling throuh menu boxes
                if event.key == pygame.K_DOWN or event.key == pygame.K_s :
                    if menuChoice < 3:
                        menuChoice += 1
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if menuChoice > 1:
                        menuChoice -= 1

                if event.key == pygame.K_RETURN:#when the player presses enter onm on of the buttons
                    if menuChoice == 1:
                        menu = False
                    if menuChoice == 2:
                        buyHp(maxHpM*15,moneyM,maxHpM,highScoreM)

                    if menuChoice == 3:
                        pygame.quit()
                        break
                        
                
            if event.type == gameGlobals.QUIT:
                pygame.quit()
                sys.exit


    player1 = player(windX/2-500,windY/2)
    moveSprite.add(player1)


    saw = obstacle(2,player1.xPos)
    obstList = [] #list of obstacles
    floorRoofList = [] #lsit of all roof and floor obj
    explosionList = [] #lists of all explotions
    collectCoinList = [] #list of all coins
    floorRoofPos = 0 

    for x in range(5): #creates roof and floor objects
        floorRoofList.append(ambientObj(0,floorRoofPos))
        floorRoofList.append(ambientObj(1,floorRoofPos))
        floorRoofPos += floorRoofList[0].size[0] #adds onto the lenght of the other steelbeam

    for x in floorRoofList:
        ambient_list.add(x)


    #music starts
    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.play(-1)
    score = 0 #score resets to 0
    while True: #game loop
        keys=pygame.key.get_pressed()
        window.fill(GREY) 

        #calling objects funtions
        moveSprite.draw(window)
        ambient_list.draw(window)
        #player jump and draw
        player1.jumpMove()
        player1.draw()

        for x in explosionList: #explosion drawing
            x.draw()
            if x.exploded == True: #animaiton finishes
                explosionList.remove(x)
                moveSprite.remove(x) #removes from moveSprite
                

        #hud icons and text 
        healthText = pixelFont.render("x" + str(player1.health),False, RED) #number of heath
        moneyText = pixelFont.render(str(player1.money),False,WHITE)
        scoreText = pixelFontSmall.render("SCORE:" + str(score),False,WHITE)
        #blit to screen
        window.blit(healthText,(0,0))#heart number
        #blit of heart image
        if player1.health >= 100:
            window.blit(heartImg,(290,0)) #heat image
        elif player1.health >= 10:
            window.blit(heartImg,(220,0)) #heart image
        else:
            window.blit(heartImg,(140,0)) #heart image

        window.blit(coinList[coinListFrame],(windX-360,0)) #coin iamge
        window.blit(moneyText,(windX-250,0)) #money text
        window.blit(scoreText,(windX/2-80,0)) #money text
        if coinFrameTrue == 3:#every other frame animates
            coinListFrame += 1
            coinFrameTrue = 1
        else:
            coinFrameTrue += 1

        if coinListFrame >= len(coinList):
            coinListFrame = 0


    #ambiant object moving
        floorRoofPos -= player1.playerSpeed #moves object as fast as player

        if len(floorRoofList) == 5 :
            floorRoofList.append(ambientObj(0,floorRoofPos))
            floorRoofList.append(ambientObj(1,floorRoofPos))
            floorRoofPos += floorRoofList[0].size[0]

        for x in floorRoofList: #draws and moves all ambiante objects
            x.draw()
            x.move(player1.playerSpeed)
            if x.xPos < -1000:
                floorRoofList.remove(x)
                ambient_list.remove(x)

            if x not in ambient_list:
                ambient_list.add(x)

        #coin object
        for x in collectCoinList:
            x.move(player1.playerSpeed)
            

            if x.collectable == True:#if the coin is collectable
                if x not in moveSprite: #if not in the move sprite group
                    moveSprite.add(x)
                x.draw()
                if pygame.sprite.collide_rect(x,player1): #collison with coin and player
                
                    player1.money = int(player1.money) + 1 #increases the money
                    score += 1 #score increase
                    #plays a sound
                    coinSound.play() 
                    #removes from both lists
                    x.collectable = False
                    moveSprite.remove(x)

            if x.xPos < -10:#removes the coin when it is out of the map
                moveSprite.remove(x)
                collectCoinList.remove(x)

            
        if len(obstList) > 0: #if an item is in obst list
            if len(collectCoinList) == 0: #if no other coins are in the list
                if obstList[0].obType == 1: #gound object
                    coinY = 200
                elif obstList[0].obType == 2: #air object
                    coinY = windY-250
                elif obstList[0].obType == 3: #wall objct
                    coinY = windY/2

                collectCoinList.append(coin(obstList[0].xPos, coinY))

        #obstical moving
        if len(obstList) == 0:
            if randint(1,3) == 1: # chance for upper obstcal to duck
                obstList.append(obstacle(2 ,windX + 50))#creates a air obstcal
            elif randint(1,3) == 2:
                obstList.append(obstacle(3 ,windX + 50)) #wall ojet
            else: 
                obstList.append(obstacle(1 ,windX + 50))#creates a ground obstcal

            if player1.playerSpeed < 25:
                player1.playerSpeed += 0.5 #speeds up the game
            elif player1.playerSpeed < 30:
                player1.playerSpeed += 0.4 #speeds up the game
            else:
                player1.playerSpeed += 0.1
        for x in obstList: #for all the obsticals
            if x not in moveSprite:
                moveSprite.add(x)
            x.draw()
            x.move(player1.playerSpeed)
            if x.xPos < +20 : #if outside  range of screen
                obstList.remove(x) #removes from obstecal list
                moveSprite.remove(x)
            
            if pygame.sprite.collide_rect(x,player1): #if a collison happens
                if x.attackable == True: #if the object is attackable+
                    if x.xPos-150 <player1.xPos < x.xPos+100:
                        if x.obType == 1: #jump obstcal
                            if player1.yPos > x.yPos -200:
                                x.attackable = False #makes the obstcal unable to attack
                                player1.health -= 1
                                hitSound.play()   
                        else:
                            x.attackable = False
                            player1.health -= 1    
                            hitSound.play()        
            if x.obType == 3: # wall type object
                for y in explosionList:
                    if pygame.sprite.collide_rect(x,y): #explotion collided with wall
                        x.attackable = False

        #keybord input
        keys=pygame.key.get_pressed() #getting all key inputs
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: #car mode when player presses s or down
            if player1.yPos > (windY /2)-200:
                player1.carMode = True
            else:
                player1.carMode = False
        else:
            player1.carMode = False

        for x in moveSprite:
            x.rect.x = x.xPos
            x.rect.y = x.yPos

        for x in ambient_list:
            x.rect.x = x.xPos
            x.rect.y = x.yPos    
            
        pygame.display.update()#refresh all draws
        clock.tick(60)
        
        for event in pygame.event.get():# quits with esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w: #can press space or w or up to jump
                    if player1.yPos > player1.minheight -70 and player1.yPos < player1.minheight: #player has to be near middle to "jump"
                        player1.jump = True
                        jumpSound.play()


                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: #can press left or d to break down walls
                    if len(explosionList) == 0: #when there are no explotions on screen
                        explosionList.append(explosion(player1.xPos+100, player1.yPos,False)) #creates an explotion
                        moveSprite.add(explosionList[0]) #add to the moveSprite list
                        explosionSound.play()#plays an explosion sound

            if event.type == gameGlobals.QUIT:
                pygame.quit()
                sys.exit
                
        #game ends if palyer dies
        if player1.health <= 0: #if the player health is zero
            pygame.mixer.music.unload()# unloads music andd stops it
            maxHpM,moneyM,highScoreM = fileWriteMenu()
            if score > highScoreM:#rewrites high score to be score
                player1.fileWrite(int(score))
            else:#score is less than high score
                player1.fileWrite(int(highScoreM))

            del(player1)#deleates player1
            pygame.sprite.Group.empty(ambient_list)
            pygame.sprite.Group.empty(moveSprite)
            obstList.clear()
            explosionList.clear()
            floorRoofList.clear()
            collectCoinList.clear()
            break
    
    loopL = True
    deathSound.play()
    while loopL:  #death loop
        

        window.fill(BLACK) #filled in 
        window.blit(gameOverText,(370,windY/2-100))
        window.blit(continueImg,(windX/2-200,windY/2+200))
        pygame.display.update()#refresh all draws
        for event in pygame.event.get():# quits with esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                if event.key == pygame.K_RETURN or event.type == pygame.K_SPACE:
                    loopL = False
            if event.type == gameGlobals.QUIT:
                pygame.quit()
                sys.exit