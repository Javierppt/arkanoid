import pygame
import os
import jugador
import pelota as BALL
import ladrillo as ld
import pygame.freetype #Libreria que usamos para escribir en pantalla
import time 
import sys #
import random as rn #generar numeros al azar
import powerup
import misil
import flechitaSAque
import pygame_menu
import ctypes

#Info del juego y Pantalla #test
WIDTH = 1280 
HEIGHT = 720



#Tupla = Letra que identifica a cada power up y su imagen
POWER_LARGE = 'L',"resources/imgLarge.png"
POWER_FUERZA = "F","resources/imgFuerza.png"
POWER_SMALL = "S","resources/imgSmall.png"
POWER_SHOOT = "M","resources/imgMissile.png"
POWER_MULTIBALL = "B","resources/imgPelotas.png"

SCR = pygame.display.set_mode((WIDTH,HEIGHT)) #inicializo la pantalla
NAME = "Jugador"
BRICK_AMOUNT = 100
BRICKS_DISTANCE =10 

COLLISION_TOLARANCE = 10

MISSILE_AMOUNT = 5
BALL_AMOUNT = 3
PAUSED = False
POWERU_UP_LIST= [POWER_FUERZA,POWER_LARGE,POWER_SMALL,POWER_SHOOT,POWER_MULTIBALL]

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
GRAY = (64,64,64)
PURPLE=(148,0,211)

BACKGROUND = pygame.image.load('resources/bg1.jpg').convert()
PLAYLIST = ["resources/venYSanaMiDolor.mp3","resources/muchachosHomero.mp3"]
#crea los ladrillos.
def createBricks(amount,powerUps): 
    posWidth = 20
    posHeight = 0   
    bricks = []
    #Genera los ladrillos
    for i in range(amount):
        brickType =rn.randrange(0,5)
        if posWidth + ld.BRICK_SIZE[0] + BRICKS_DISTANCE  > WIDTH:
            posWidth = 20
            posHeight += ld.BRICK_SIZE[1] + 20    
        if brickType == 0:
            redBrick = ld.normalBrick("resources/ladrilloRojo.png",posWidth,posHeight, 1,1)
            brickGroup.add([redBrick])
            del redBrick
        elif brickType == 1:
            greenBrick = ld.normalBrick("resources/ladrilloVerde.png",posWidth,posHeight, 2,2)
            brickGroup.add([greenBrick])
            del greenBrick
        elif brickType==2:
            num = rn.randrange(0,len(powerUps))
            violetBrick = ld.ladrillo_p("resources/ladrilloVioleta.png",posWidth,posHeight, 1,2,POWERU_UP_LIST[num][0],POWERU_UP_LIST[num][1])
            brickGroup.add([violetBrick])
            del violetBrick
            del num
        elif brickType == 3:
            blueBrick = ld.normalBrick("resources/ladrilloAzul.png",posWidth,posHeight, 3,3)
            brickGroup.add([blueBrick])
            del blueBrick
        elif brickType == 4:
            grayBrick = ld.fallingBrick("resources/ladrilloGris.png",posWidth,posHeight, 4,4)
            brickGroup.add([grayBrick])
            del grayBrick
        posWidth += ld.BRICK_SIZE[0] + BRICKS_DISTANCE
    return bricks

#suma los puntos al puntaje total.
def addScore(pts):
    global SCORE
    SCORE += pts






#Dibuja el puntaje en la pantalla.
def drawScore():

    text_surface, rect = GAME_FONT.render("Puntaje: " + str(SCORE), WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.15
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect)

#Dibuja el numero de vidas del jugador en la pantalla.
def drawLives():
    text_surface, rect = GAME_FONT.render("Vidas: " + str(lives), WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.05
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect, )

def drawName():
    text_surface, rect = GAME_FONT.render("Nombre: " + NAME, WHITE)
    rect.x = 0
    rect.y = HEIGHT / 1.25
    SCR.blit(BACKGROUND, rect, rect)
    SCR.blit(text_surface, rect )

#Deja la pelota arriba del jugador, esperando al saque.
def serve(player,ball):
    SCR.blit(BACKGROUND, ball.rect, ball.rect) 
    ball.rect.midbottom = player.rect.midtop
    SCR.blit(ball.image, ball.rect) 
    ball.verticalSpeed = 0
    ball.horizontalSpeed = 0

#Texto de cuando el jugador pierde.
def gameOver():
    global playing
    global menu
    text_surface, rect = GAME_FONT.render("GAME OVER", WHITE, size = 100)
    rect.centerx = WIDTH / 2
    rect.centery = HEIGHT / 2
    SCR.blit(text_surface, rect )
    
    pygame.display.flip()
    time.sleep(3)
    playing = False
    menu.enable()



#Texto de cuando el jugador gana.
def win():
    global playing
    global menu
    text_surface, rect = GAME_FONT.render("GANASTE", WHITE, size = 100)
    rect.centerx = WIDTH / 2
    rect.centery = HEIGHT / 2
    SCR.blit(text_surface, rect )
    
    pygame.display.flip()
    time.sleep(3)
    playing = False
    menu.enable()

#Rompe al ladrillo cuando algo le pega (pelota o power up de los tiros).
def breakBrick(brk,proyectile):
    brk.setResistance(brk.getResistance()-proyectile.strenght)
    #Esto que comente hace que el ladrillo se rompa cuando todavia tiene 2 de vida
    #if brk.resistance <= proyectile.strenght: # 3 3
        #brk.resistance = 0
    if brk.resistance <= 0:
        brk.breakSound.play()
        return brk.points
    else:
        return 0



#Rebote vertical.
def bounceV(brk, b):
    SCR.blit(BACKGROUND, b.rect, b.rect)
    b.invertVSpeed()
    b.move()
    SCR.blit(b.image, b.rect)
    SCR.blit(brk.image, brk.rect)

#Rebote horizontal.
def bounceH(brk, b):
    SCR.blit(BACKGROUND, b.rect, b.rect)
    b.invertHSpeed()
    b.move()
    SCR.blit(b.image, b.rect)
    SCR.blit(brk.image, brk.rect)

#Agrega un power up al grupo de los power ups.
def addPowerUp(points,powerUpGroup,brick,SCR):
    if points > 0:
                SCR.blit(BACKGROUND, brick.rect, brick.rect)
                brickGroup.remove(brick)
                addScore(points)
                if isinstance(brick, ld.ladrillo_p):
                    powerUpGroup.add([powerup.powerUp(brick.rect.x, brick.rect.y, brick.powerUp,brick.imagenPU)])

#Cambia el color de los ladrillos segun la resistencia que le queda.
def resistenceColor(brick,SCR):
    try:
        brick.resistanceColor()
        SCR.blit(BACKGROUND, brick.rect, brick.rect)
        SCR.blit(brick.image,brick.rect)
    except Exception as e:
            pass
    
#Verifica si un ladrillo es de la clase ladrillo flojo.
def isFallingBrick(SCR,proyectile,brick):
    #Verifica si el ladrillo es de la clase ladrillo flojo
    if isinstance(brick, ld.fallingBrick):
        SCR.blit(BACKGROUND, proyectile.rect, proyectile.rect)
        brick.setFalling(True)
        SCR.blit(proyectile.image,proyectile.rect)


def multiBall(SCR,ballGroup,b,BALL_AMOUNT):
        for i in range(BALL_AMOUNT):
            if not len(ballGroup)>=BALL_AMOUNT:
                if i % 2 == 0:
                    ballGroup.add(BALL.Pelota((b.rect.x+b.rect.width),b.rect.y))
                else:
                    ballGroup.add(BALL.Pelota((b.rect.x-b.rect.width),b.rect.y))
        i = 0
        for ball in ballGroup: 
            ball.setSpeed(b.getSpeed()[0],b.getSpeed()[1])
            i +=1
            if i != 0:
                if i % 2 == 0:
                    ball.invertHSpeed()
                if i % 2 != 0:
                    ball.invertVSpeed()



def updateBallPosition(SCR,ball):
    SCR.blit(BACKGROUND, ball.rect, ball.rect)
    ball.move()
    SCR.blit(ball.image, ball.rect) 

def settingsMenu():
    menu._open(settings)

def infoMenu():
    menu._open(info)

def start_the_game():
    global playing
    global menu
    menu.disable()
    playing = True

def pause(PAUSE):
    if PAUSE:
        return False
    else:
        return True

    

def config(brickAmount,livesAmount,missileAmount,ballAmount,name,fullScreen = False):
    global BRICK_AMOUNT
    global lives
    global NAME
    global MISSILE_AMOUNT
    global BALL_AMOUNT
    global BACKGROUND
    global HEIGHT
    global WIDTH
    global SCR

    if fullScreen:
        SCR = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
    else:
        SCR = pygame.display.set_mode((WIDTH,HEIGHT))
    BALL_AMOUNT = ballAmount
    BRICK_AMOUNT = brickAmount
    lives = livesAmount
    MISSILE_AMOUNT = missileAmount
    NAME = name

#Elige una cancion aleatoria y la reproduce.Cuando termina una sigue con otra.
def playList():
    global PLAYLIST
    
    rn.shuffle(PLAYLIST)

    pygame.mixer.music.load ( PLAYLIST.pop() )  
    pygame.mixer.music.queue ( PLAYLIST.pop() ) 
    
    pygame.mixer.music.set_volume(.3)
    pygame.mixer.music.play() 


def game():
    global PAUSED
    global BACKGROUND
    global NAME
    global ball
    global player
    global ballGroup
    global brickGroup
    global playerGroup
    global missileGroup
    global powerUpGroup
    global playing
    global BALL_AMOUNT
    global waitingServe
    global shootPU
    global lives
    global MISSILE_AMOUNT
    global PLAYLIST
    #Bucle principal
    while playing:
        #Eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:    
                if len ( PLAYLIST ) > 0:      
                    pygame.mixer.music.queue ( PLAYLIST.pop() ) 
            #Cierra el juego con la cruz
            if event.type == pygame.QUIT:
                pygame.quit()        
                playing = False
                sys.exit()
            #Eventos de apretar una tecla
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE and waitingServe):
                    waitingServe = False     
                    ball.serve(flecha.angle)  
                elif  (event.key == pygame.K_ESCAPE):
                    pygame.display.toggle_fullscreen()
                    SCR.blit(BACKGROUND,(0,0))
                    #Esto hace que cuando se cambia de pantalla completa a ventana o al reves, no desaparezcan los ladrilllos
                    for brick in brickGroup:
                        SCR.blit(brick.image,brick.rect)
                    pygame.display.flip()
                elif (event.key == pygame.K_p):
                    PAUSED = pause(PAUSED) 
                elif (event.key == pygame.K_SPACE and not waitingServe and shootPU):
                    missile = misil.Misille(player.rect.centerx,player.rect.y)                
                    missileGroup.add([missile])
                    player.setShoot(player.getShoot()-1)
                    if player.getShoot() == 0:
                        shootPU = False

        joystick = pygame.key.get_pressed()
        
        if PAUSED:
            pass
        else:
            #Movimiento del jugador
            if joystick[pygame.K_LEFT]:
                SCR.blit(BACKGROUND, player.rect, player.rect)
                player.moveLeft(0)
                SCR.blit(player.image, player.rect) 
            elif joystick[pygame.K_RIGHT]:
                SCR.blit(BACKGROUND, player.rect, player.rect)
                player.moveRight(WIDTH-10)
                SCR.blit(player.image, player.rect)
            
            #SAque del jugador. si el jugador saco, mueve la pelota
            if waitingServe == True:
                joystick = pygame.key.get_pressed()
                SCR.blit(BACKGROUND,(0,0))
                SCR.blit(player.image,player.rect)
                for brick in brickGroup:
                    SCR.blit(brick.image,brick.rect)
                flecha.update(1,joystick)
                flecha.draw(SCR,player.rect.centerx, player.rect.centery - ball.rect.height)
                serve(player,ball)

            #Choque con el jugador
            if pygame.sprite.spritecollideany(player, ballGroup):
                for ball in ballGroup:               
                    if abs(ball.rect.top - player.rect.bottom) < COLLISION_TOLARANCE and ball.verticalSpeed < 0:
                        bounceV(player, ball)

                        if abs(ball.rect.bottom - player.rect.top) < COLLISION_TOLARANCE and ball.verticalSpeed > 0:
                            bounceV(player, ball)

                        if abs(ball.rect.left - player.rect.right) < COLLISION_TOLARANCE and ball.horizontalSpeed < 0:
                            bounceH(player, ball)
                    if abs(ball.rect.bottom - player.rect.top) < COLLISION_TOLARANCE and ball.verticalSpeed > 0:
                        if ball.rect.centerx < player.rect.centerx :
                            if ball.horizontalSpeed < 0:
                                ball.horizontalSpeed -= 0.5
                            else:
                                ball.horizontalSpeed = BALL.Pelota.getDefaultSpeed()
                        elif ball.rect.centerx > player.rect.centerx :
                            if ball.horizontalSpeed > 0:
                                ball.horizontalSpeed += 0.5
                            else:
                                ball.horizontalSpeed = BALL.Pelota.getDefaultSpeed()
                        bounceV(player, ball)
                    if abs(ball.rect.left - player.rect.right) < COLLISION_TOLARANCE and ball.horizontalSpeed < 0:
                        bounceH(player, ball)

                        if abs(ball.rect.right - player.rect.left) < COLLISION_TOLARANCE and ball.horizontalSpeed > 0:
                            bounceH(player, ball)

            #Choque con limite de la pantalla
            for ball in ballGroup:
                if ball.rect.top < 0 - COLLISION_TOLARANCE and ball.verticalSpeed < 0 :
                    ball.invertVSpeed()
                if abs(ball.rect.right - WIDTH) < COLLISION_TOLARANCE and ball.horizontalSpeed > 0:
                    ball.invertHSpeed()
                if abs(ball.rect.left+10) < COLLISION_TOLARANCE and ball.horizontalSpeed < 0:
                    ball.invertHSpeed()

            for ball in ballGroup:
                updateBallPosition(SCR,ball)

            #Rebote de las pelotas con los ladrillos 
            for ball in ballGroup:                
                collisionedBricks = pygame.sprite.spritecollide(ball, brickGroup, False)
                if len(collisionedBricks) > 0:
                    ball.bounce.play()  
                    for brick in collisionedBricks:
                        SCR.blit(brick.image, brick.rect)
                        if ball.strenght > 1:
                            ball.strenght-= brick.resistance
                            points = breakBrick(brick,ball)    
                            if ball.strenght <= 0:
                                ball.strenght = 1
                            SCR.blit(BACKGROUND, ball.rect, ball.rect)
                            SCR.blit(ball.image, ball.rect)
                            SCR.blit(BACKGROUND, brick.rect, brick.rect)
                        else:
                            #si pelota fuerza == 1
                            if abs(ball.rect.top - brick.rect.bottom) < COLLISION_TOLARANCE and ball.verticalSpeed < 0:
                                bounceV(brick, ball)
                                points = breakBrick(brick,ball)
                            if abs(ball.rect.bottom - brick.rect.top) < COLLISION_TOLARANCE and ball.verticalSpeed > 0:
                                bounceV(brick, ball)
                                points = breakBrick(brick,ball)
                            if abs(ball.rect.left - brick.rect.right) < COLLISION_TOLARANCE and ball.horizontalSpeed < 0:
                                bounceH(brick, ball)
                                points = breakBrick(brick,ball)
                            if abs(ball.rect.right - brick.rect.left) < COLLISION_TOLARANCE and ball.horizontalSpeed > 0:
                                bounceH(brick, ball)
                                points = breakBrick(brick,ball)
                    
                        resistenceColor(brick,SCR)
                        addPowerUp(points,powerUpGroup,brick,SCR)
                        if (points>0): 
                            addScore(points)
                        isFallingBrick(SCR,ball,brick)
                        
                    

            #Ladrillo flojo. si se choco una vez, se cae. Si le pega al jugador le resta una vida.
            #Si el ladrillo se va por abajo del jugador sin pegarle se elimina
            for brick in brickGroup:
                if isinstance(brick, ld.fallingBrick) and brick.falling:
                        SCR.blit(BACKGROUND, brick.rect, brick.rect)
                        brick.fall()
                        SCR.blit(brick.image,brick.rect)   
                if pygame.sprite.spritecollideany(brick, playerGroup):
                    lives -= 1
                    SCR.blit(BACKGROUND, brick.rect, brick.rect)
                    brickGroup.remove(brick)
                    waitingServe = True   
                    serve(player,ball)
                    SCR.blit(BACKGROUND,flecha.rect,flecha.rect)
                if brick.rect.y > HEIGHT + 10:
                    SCR.blit(BACKGROUND, brick.rect, brick.rect)
                    brickGroup.remove(brick)
                    del brick

            #tira los tiros
            if (shootPU or len(missileGroup)>0):
                try:        
                    for m in missileGroup:    
                        SCR.blit(BACKGROUND,m.rect,m.rect)
                        m.lauch() 
                        SCR.blit(m.image,m.rect)
                        if m.rect.y < 0 - m.rect.height - 40:
                            missileGroup.remove(m)
                            del m      
                except Exception as e:
                    pass

            

            #Choque de los tiros con los ladrillos
            for m in  missileGroup:   
                crashedBrick = pygame.sprite.spritecollideany(m, brickGroup)
                if crashedBrick:           
                        points = breakBrick(crashedBrick,m)
                        addPowerUp(points,powerUpGroup,crashedBrick,SCR)
                        resistenceColor(crashedBrick,SCR)
                        isFallingBrick(SCR,m,crashedBrick)
                        if points > 0:
                            brickGroup.remove(crashedBrick)    
                        SCR.blit(BACKGROUND, crashedBrick.rect, crashedBrick.rect)
                        missileGroup.remove(m)
                        SCR.blit(BACKGROUND,m.rect,m.rect)
                        del m

            #hace caer al power up
            if len(powerUpGroup) > 0:
                for power in powerUpGroup:
                    SCR.blit(BACKGROUND, power.rect, power.rect)
                    power.fallDown()    
                    SCR.blit(power.image, power.rect)
                    for brick in brickGroup:
                        SCR.blit(brick.image,brick.rect)

            #Verifica si el power up que cae choca con el jugador
            powerUpColisioned = pygame.sprite.spritecollide(player, powerUpGroup, True)
            #si choca, le da el power up al jugador
            if len(powerUpColisioned) > 0:
                for power in powerUpColisioned:
                    SCR.blit(BACKGROUND, powerUpColisioned[0], powerUpColisioned[0])
                    if powerUpColisioned[0].powerUp == POWER_LARGE[0]:
                        SCR.blit(BACKGROUND, player.rect, player.rect)
                        player.getBig()
                        SCR.blit(player.image, player.rect)
                    elif powerUpColisioned[0].powerUp == POWER_FUERZA[0]:
                        ball.strengthUp()
                    elif powerUpColisioned[0].powerUp == POWER_SMALL[0]:
                        SCR.blit(BACKGROUND, player.rect, player.rect)
                        player.getSmall()
                        SCR.blit(player.image, player.rect)
                    elif powerUpColisioned[0].powerUp == POWER_SHOOT[0]:
                        player.setShoot(MISSILE_AMOUNT)
                        shootPU = True
                    elif powerUpColisioned[0].powerUp == POWER_MULTIBALL[0]:
                        if not waitingServe:
                            multiBall(SCR,ballGroup,ball,BALL_AMOUNT)
                            updateBallPosition(SCR,ball)
                        else:
                            pass

                    SCR.blit(BACKGROUND, power, power)
                    powerUpGroup.remove(power)

                    
                    
            drawName()
            drawScore()
            drawLives()
            
            #Actualiza la pantalla
            pygame.display.flip()


            
            if len(ballGroup) == 0:
                lives -=1

            if len(ballGroup)>=2:
                for ball in ballGroup:
                        if ball.rect.y > HEIGHT + 20:
                            ballGroup.remove(ball)
                            del ball

            #Si la pelota se cae por abajo el jugador pierde una vida. Si pierde todas las vidas pierde el juego.
            if len(ballGroup) == 1:
                for ball in ballGroup:
                    if ball.rect.top > HEIGHT + 20:
                        if lives > 1:
                            lives -=1
                            waitingServe = True   
                            serve(player,ball)
                            SCR.blit(BACKGROUND,flecha.rect,flecha.rect)
                        else:
                            gameOver()
                
            #condicion para ganar el juego
            if len(brickGroup) == 0:
                win()

            if lives == 0:
                    gameOver()
            
            
            
            clock.tick(60)


pygame.init()

GAME_FONT = pygame.freetype.SysFont('roboto', 20, bold=False, italic=False)

clock = pygame.time.Clock()



playing = False
playList()
#Bucle del menu
while not playing:

    #resolucion actual de la pantalla
    """user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    resH, resV = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)"""

    
    lives = 3
    points = 0
    brickGroup  = pygame.sprite.Group()
    
    brickGroup.draw(SCR)
    SCORE = 0
    ballGroup = pygame.sprite.Group()
    
    playerGroup = pygame.sprite.Group()
    
    waitingServe = True

    shootPU = False
      
    missileGroup = pygame.sprite.Group()
    powerUpGroup = pygame.sprite.Group() 
    
    menu = pygame_menu.Menu('Arkanoid',WIDTH, HEIGHT)

    menu.add.text_input('Name :', default=NAME,textinput_id="nombreJugador")
    menu.add.button('Play',start_the_game )
    menu.add.button('Settings',settingsMenu)
    menu.add.button('Info',infoMenu)
    menu.add.button('Quit',pygame_menu.events.EXIT)

    settings = pygame_menu.Menu('Arkanoid',WIDTH, HEIGHT)
    
    settings.add.range_slider('Cantidad de ladrillos :', 50,(10,100),int(2),rangeslider_id="cantLadrillos")
    settings.add.range_slider('Cantidad de vidas :', 3,(1,10),int(1),rangeslider_id="cantVidas")
    settings.add.range_slider('Cantidad de tiros (Power UP) :', 5,(1,10),int(1),rangeslider_id="cantTiros")
    settings.add.range_slider('Cantidad de pelotas (Power UP) :', 3,(1,5),int(1),rangeslider_id="cantPelotas")
    settings.add.toggle_switch('Full screen (ESC en el juego):',toggleswitch_id="fullScreen",default=False,state_text=("NO","SI"))
    settings.add.button('Volver',pygame_menu.events.BACK)

    info = pygame_menu.Menu('Arkanoid',WIDTH, HEIGHT)
    info.center_content()
    info.add.label("Flecha izquierda/ flecha derecha: Movimiento del jugador")
    info.add.label("A/D: Control de la direccion del saque")
    info.add.label("Espacio: Saque")
    info.add.label("ESC: Cambiar entre pantalla completa y modo ventana")
    info.add.label("P: Pausa")
    info.add.label("Escapcio: Usa power Up de los tiros (Cuando la pelota esta en juego) ")
    info.add.button("Volver",pygame_menu.events.BACK)

    music = pygame_menu.Menu('Arkanoid',WIDTH, HEIGHT)
    
    
    
    menu.enable()
    menu.mainloop(SCR)
    

    settings.render()
    
        
    SCR.blit(BACKGROUND,(0,0))
    if playing:
        angle = 0
        
        config(int(settings.get_widget("cantLadrillos").get_value()),
               int(settings.get_widget("cantVidas").get_value()),
               int(settings.get_widget("cantTiros").get_value()),
               int(settings.get_widget("cantPelotas").get_value()),
               menu.get_widget("nombreJugador").get_value(),
               settings.get_widget("fullScreen").get_value()
               )
        
        
        player = jugador.Jugador((WIDTH /2),HEIGHT -50)
        playerGroup.add([player])
        ball = BALL.Pelota(WIDTH /2,HEIGHT/2)
        ballGroup.add([ball])
        flecha = flechitaSAque.FlechitaSaque(player.rect.centerx, player.rect.centery - ball.rect.height, 80, 10)
        
        brickGroup.add( [createBricks(BRICK_AMOUNT,POWERU_UP_LIST)])
         
        SCR.blit(BACKGROUND, (0, 0))
        SCR.blit(BACKGROUND, ball.rect, ball.rect) 
        SCR.blit(player.image, player.rect)
        
        game()
    
pygame.quit()