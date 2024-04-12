import math, random
import pygame as pg 
from sys import exit
from settings import *

class Player():
    def __init__(self):
        super().__init__()
        self.image= pg.transform.rotozoom(pg.image.load("player/leo.png").convert_alpha(), 0, PLAYER_SIZE)
        self.pos= pg.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed= PLAYER_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        pass

    def user_input(self):
        self.velocity_x= 0
        self.velocity_y=0

        keys = pg.key.get_pressed()

        if keys[pg.K_w] and self.pos.y >= 0:
            self.velocity_y=-self.speed
        if keys[pg.K_s] and self.pos.y <= ALTURA-self.image.get_height():
            self.velocity_y= self.speed
        if keys[pg.K_d] and self.pos.x <= ANCHO-self.image.get_width():
            self.velocity_x= self.speed
        if keys[pg.K_a] and self.pos.x >= 0:
            self.velocity_x= -self.speed

        if self.velocity_x !=0 and self.velocity_y !=0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
        


    def move(self):
        self.pos += pg.math.Vector2(self.velocity_x, self.velocity_y)
    
    def update(self):
        self.user_input()
        self.move()

class object():
    def __init__(self,image_path):
        super().__init__()
        self.image= pg.transform.rotozoom(pg.image.load(image_path).convert_alpha(),0,OBJECT_SIZE)      
        self.image.set_colorkey()
        self.rect= self.image.get_rect()
        OBJECT_START_X = random.randint(0, ANCHO - self.image.get_width())
        self.pos = pg.math.Vector2(OBJECT_START_X, OBJECT_START_Y)
        self.speed = OBJECT_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.pos)
    
    def move(self):
        self.pos.y+=self.speed

    def update(self):
        self.move()

class Object_spawner():
    def __init__(self):
        self.list= ["Objects/goku_supreme.png","Objects/vegeta_supreme.png"]
        self.objects=[]
        for i in self.list:
            self.objects.append(object(i))

    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)

    def update(self):
        for obj in self.objects:
            obj.move()

    def new_obj(self):
        random.shuffle(self.list)
        self.objects.append(object(self.list[0]))

"""
def colision(player, object): #colision del objeto y el jugador
    if player.x <  (object.x + object.image.get_width()) and \
       player.x + player.image.get_width() > object.x and \
       player.y <  (object.y + object.image.get_height()) and \
       player.y + player.image.get_height() > object.y :
           return True
    else:
        return False
"""

def main(): # Todo el código
    pg.init()

    #Pantalla
    screen = pg.display.set_mode((ANCHO , ALTURA))
    pg.display.set_caption("Top Down Game")
    clock= pg.time.Clock()

    # Fondos
    background = pg.transform.scale(pg.image.load("Background/floor_demo.jpg").convert(), (ANCHO, ALTURA))
    background_pausa = pg.transform.scale(pg.image.load("Background/Pausa.png").convert(), (ANCHO, ALTURA))

    # Colores
    White=(255,255,255)
    Black=(0,0,0)
    Red=(255,0,0)
    Blue=(0,0,255)
    Magenta= (255, 0, 255)
    Cian= (0, 255, 255)

    # Texto
    font= pg.font.SysFont("Comic Sans MS", 150)
    font_1=pg.font.SysFont("Comic Sans MS", 75)
    text=font.render("PAUSE", True, Cian)
    text_2=font_1.render("PRESIONA C PARA CONTINUAR", True, Cian)
    text_3=font_1.render("PRESIONA P PARA PAUSAR", True, White)
    
    # Música
    game_music = pg.mixer.Sound("Sound/Sans_theme.mp3") 
    pause_music = pg.mixer.Sound("Sound/Guaremate.mp3") 

    game_music.set_volume(VOLUMEN)
    pause_music.set_volume(VOLUMEN)
    
    pg.mixer.Channel(1).play(game_music, loops=-1)

    pg.mixer.Channel(2).play(pause_music, loops=-1)
    pg.mixer.Channel(2).pause()

    # Clases
    player = Player()
    object_spawner= Object_spawner()

    isPaused = False
    musicStarted = False

    deltaTime = 0
    timeElapsed = 0

    def pause():
        screen.blit(background_pausa, (0, 0))
        screen.blit(text, (\
            (ANCHO - text.get_width())/2,\
            -200 + (ALTURA - text.get_height())/2\
            ))
        screen.blit(text_2, (\
            (ANCHO - text_2.get_width())/2,\
            300 + (ALTURA - text_2.get_height())/2\
            ))

    def play(deltaTime, timeElapsed):
        
        timeElapsed += deltaTime
        if (timeElapsed >= 1500):
            timeElapsed = 0
            object_spawner.new_obj()

        player.update()
        object_spawner.update()
        screen.blit(background, (0, 0))
        player.draw(screen)
        object_spawner.draw(screen)
        screen.blit(text_3, (\
            -95 + (ANCHO - text_3.get_width())/2,\
            300 + (ALTURA - text_3.get_height())/2\
            ))
        
        return timeElapsed
    
    # Mainloop

    while True:
        clock.tick()
        for event in pg.event.get(): # Event Poll
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type==pg.KEYUP:
                if event.key==pg.K_p:
                    isPaused = True
                    pg.mixer.Channel(2).unpause()
                    pg.mixer.Channel(1).pause()
                       
                if event.key==pg.K_c:
                    isPaused = False
                    pg.mixer.Channel(1).unpause()
                    pg.mixer.Channel(2).pause()
            """
            elif event.type == pygame.KEYDOW:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    """

        keys = pg.key.get_pressed()

        """
        hits= pygame.sprite.spritecollide(Player, object, True) #Colisiones del objeto y el jugador
        if hits:
            runnig = False
        """
        if isPaused:
            pause()

        else:
            timeElapsed = play(deltaTime, timeElapsed)

        pg.display.flip()
        pg.display.update()

        clock.tick(Fps)
        deltaTime = clock.get_time()

    pass

if __name__ == '__main__':
    main()
