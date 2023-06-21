from settings import *
from tetrominos import Tetromino
import math
import pygame.freetype as ft

class Text:
    #definicion de tipo de letra
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    #dibujo de los texto dentro del juego
    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02), text='TETRIS', fgcolor='white', size=TILE_SIZE * 1.10, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22), text='Next', fgcolor='white', size=TILE_SIZE * 1.2, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67), text='Score', fgcolor='white', size=TILE_SIZE * 1.2, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8), text=f'{self.app.tetris.score}', fgcolor='white', size=TILE_SIZE * 1.4, bgcolor='black')

#incialiacion de la clase tetris
class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pygame.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        self.score = 0
        self.full_lines = 0
        #lista de valores de scores de lineas
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3:700, 4:1500}

    #scores los cuales se suma las lineas que se hicieron y despues se les devuelve el valor del numero que hay en la lista para agregar al score
    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    #verificacion de que hay una linear, entendimiento en proceso ###################################
    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y) 

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    #creacion de bloque en el lugar donde esta el tetromino remplazando el 0 del espacio vacio, para la implementacion de colision
    #0 0 0 0
    #0 0 B 0
    #0 0 B 0
    #0 B B 0
    def put_tetromino_block_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    #crea toda el area de juego con 0 para decir que es un espacio vacio
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    #si un bloque de la clase blocks de la figura del tetromino se crea/posisiona en el mismo
    #lugar donde aparecen lo bloques, envia true para que se reinicia el juego
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OOFSET[1]:
            pygame.time.wait(300)
            return True
        
    #verifica despues de que el tetromino aterrizo si hay game over para reiniciar el juego,
    #pone la velocidad normal de vuelta de caida
    #loquea el lugar donde esta el tetromino
    #hace aparecer el siguiente tetromino que tenia que aparecer
    #cambia el siguiente tetromino a mostrar
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_block_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    #controles del jugador
    def control(self, pressed_key):
        if pressed_key == pygame.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pygame.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pygame.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pygame.K_DOWN:
            self.speed_up = True

    #dibujo de los rectangulos en la zona de juego en el fondo par un mayor entendimiento de las propiedades
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pygame.draw.rect(self.app.screen, 'blue',(x * TILE_SIZE,y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    #actualizador encargado de verificar si se hice una linea, actualizar el estado del tetromino, verificar que aterrise y que obtenga el score mientras esta cayendo
    #cuando termina de caer se loquea el sitio del tetromino
    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    #dibujo de los rectangulos de fondo del area de juego, dibujo de las imagenes en los bloques del tetromino
    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)