from settings import *
from tetri import Tetris, Text
from button import Button
import sys
import pathlib

class App:
    #inicializacion de toda la aplicacion
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode(WIN_RES)
        self.clock = pygame.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)

        #musica
        pygame.mixer.music.load('tetrispygame/Music/TetrisTheme.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    #creacion de lista de imagenes con filtrado de extension de archivo y configuracion de las imagenes de conversion a alpha y escalado de la misma
    def load_images(self):
        files = [item for  item in pathlib.Path(SPRITE_PATH).rglob('*.png') if item.is_file()]
        images = [pygame.image.load(file).convert_alpha() for file in files]
        images = [pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    #definicion de variable para la velocidad en la que baja el tetromino
    def set_timer(self):
        self.user_event = pygame.USEREVENT + 0
        self.fast_user_event = pygame.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pygame.time.set_timer(self.user_event, ANIM_TIME_INTERVALE)
        pygame.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVALE)

    #actualizador general actualiza los fps (llama al actualizador de la clase tetris)
    def update(self):
        self.tetris.update()    
        self.clock.tick(FPS)
    
    #dibujador general
    #color de fondos
    #(llamado de los dibujadores de las clases tetris y test)
    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, * FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pygame.display.flip()
    
    #verificador de eventos de salir del juego, controles de movimiento e cambio entre velocidad entre normal y rapida 
    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


SCREEN = pygame.display.set_mode((WIN_RES))

pygame.init()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("tetrispygame/Font/fontaa.ttf", size)

def main_menu():
    while True:
        SCREEN.fill(color=BG_COLOR)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("tetrispygame/Sprites/violeta.png"), pos=(450, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4")
        OPTIONS_BUTTON = Button(image=pygame.image.load("tetrispygame/Sprites/violeta.png"), pos=(450, 500), 
                            text_input="SCOREBOARD", font=get_font(75), base_color="#d7fcd4")
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON]:    
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    app = App()
                    app.run()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass

        pygame.display.update()

main_menu()
      