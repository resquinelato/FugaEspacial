"""
Jogo: Fuga Espacial.
Descrição: Um grupo de diplomatas escapam de uma fortaleza estalar a bordo de uma nave danificada.
A nave precisa se desviar das ameaças e sobreviver até atingir a zona de segurança diplomática.
"""

import pygame
import time #uso da função-membro time.sleep(...) in loop
import random

class Background:
    """
    Esta classe define o Plano de fundo do jogo
    """
    image = None #atributo
    margin_left = None
    margin_right = None

    def __init__(self):
        
        background_fig = pygame.image.load("FugaEspacial/Images/background.png")
        background_fig.convert() #convert a imagem no display
        background_fig = pygame.transform.scale(background_fig, (800,602))
        self.image = background_fig #atribui a imagem para o background
    
        margin_left_fig = pygame.image.load("FugaEspacial/Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60,602))
        #margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602)) #redimensiona a imagem da margem
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("FugaEspacial/Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_right_fig, (60, 602)) #redimensiona a imagem da margem
        self.margin_right = margin_right_fig    

    # __init__()

    def update(self, dt):
        pass
    # update()

    def draw(self, screen): 
        # os objetos são desenhados na tela pelo metodo blit
        # copia dados de imagem de uma superfície pra outra
        # esse metodos desenha objetos que são exibistos apos o .update()
        screen.blit(self.image, (0,0)) #imagem do background na tela para a cordenada 0,0
        screen.blit(self.margin_left, (0,0)) # 60 depois da primeira margem
        screen.blit(self.margin_right, (740, 0)) # 60 depois da segunda margem
    # draw()

    # Define posições das imagens do Plano de fundo para criar movimentos
    def move(self, screen, scr_height, movL_x, movL_y, movR_x, movR_y):
        #movimento do backdroud em 3 blocos contínuos
        for i in range(0, 2):
            screen.blit(self.image, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_left, (movL_x, movL_y - i * scr_height))
            screen.blit(self.margin_right, (movR_x, movR_y - i * scr_height))
# Background


class Player:
    """
    Esta classe define o Jogador
    """
    image = None # inicializa atributos do jogador
    x = None
    y = None

    def __init__(self, x, y):
        player_fig = pygame.image.load("FugaEspacial/Images/player.png")
        player_fig.convert()
        player_fig = pygame.transform.scale(player_fig, (90,90))
        self.image = player_fig
        self.x = x
        self.y = y
    # __init__()

    # Desenhar Player
    def draw (self, screen, x, y): # método para desenhar Player
        screen.blit(self.image, (x, y)) 
#Player

class Hazard:
    """
    Esta classe define Ameaça ao jogador
    """
    image = None
    y = None
    x = None
    
    def __init__(self, img, x, y):
        hazard_fig = pygame.image.load(img)
        hazard_fig.convert()
        hazard_fig = pygame.transform.scale(hazard_fig, (130, 130))
        self.image = hazard_fig
        self.x = x
        self.y = y
    # __init__()
    
    def draw (self, screen, x, y):
        screen.blit(self.image, (x,y))
    # draw
# Hazard



class Game:
    screen = None #inicializar atributos
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None
    player = None # atributo player
    hazard = []
    render_text_bateulateral = None
    render_text_perdeu = None

    # Movimento do Player
    DIREITA = pygame.K_RIGHT
    ESQUERDA = pygame.K_LEFT
    mudar_x = 0.0

    def __init__(self, size, fullscreen):

        """
        Função que inicializa o pygame, define a resolução da tela,
        caption e desabilita o mouse
        """ 
        # Operações
        pygame.init() #inicializar o pygame

        self.screen = pygame.display.set_mode((self.width, self.height)) #tamanho da tela
        self.screen_size = self.screen.get_size() #define o tamnho da tela do jogo

        pygame.mouse.set_visible(0) # desabilita o mouse
        pygame.display.set_caption('Fuga Espacial')

        # define as fontes
        my_font = pygame.font.Font("FugaEspacial/Fonts/Fonte4.ttf", 100)

        # Mensagens para o jogador
        self.render_text_bateulateral = my_font.render("VOCê BATEU!", 0,(255, 255, 255)) #(texto, opaco/transparente 0/1, cor do texto )
        self.render_text_perdeu = my_font.render("GAME OVER!", 0, (255, 0, 0)) # (texto, opaco/transparente 0/1, cor do texto)      
    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():

            # interromper o jogo quando clicar em fechar
            if event.type == pygame.QUIT:
                self.run = False 

            # se clicar em qualquer tecla, entra no if
            if event.type == pygame.KEYDOWN:

                # se clicar na seta a esquerda, anda 3 para esquerda no eixo x
                if event.key == self.ESQUERDA:
                    self.mudar_x = -3

                # se clicar na seta a direita, anda 3 para direita no eixo x
                if event.key == self.DIREITA:
                    self.mudar_x = 3
            
            # se soltar qualquer tecla nao faz nada
            if event.type == pygame.KEYUP:
                if event.key == self.ESQUERDA or event.key == self.DIREITA:
                    self.mudar_x = 0
    # handle_events()

    def elements_update(self, dt):
        self.background.update(dt) #atualziar elementos
    # elements_update()

    def elements_draw(self):
        self.background.draw(self.screen) #desenhar elementos
    # elements_draw()

    def loop(self):
        """
        Laço principal
        """
        
        # variaveis para movimento plano de fundo/inimigos
        velocidade_background = 10
        velocidade_hazard = 10

        # movimento da margem esqueda / também para plano de fundo
        movL_x = 0
        movL_y = 0

        # movimento da margem direita / também para plano de fundo
        movR_x = 740
        movR_y = 0

        hzrd = 0
        h_x = random.randrange(125, 660)
        h_y = -500 # localização

        # Info Hazard (dimensão)
        h_width = 100
        h_height = 110

        # Criar o plano de fundo
        self.background = Background() # cria o objeto background

        # Posicao do Player
        x = (self.width - 56) / 2
        y = (self.height - 125)

        # Criar o Player
        self.player = Player(x, y)

        # Criar os Hazards (inimigos) adiciona elemento na lista
        self.hazard.append(Hazard("FugaEspacial/Images/satelite.png", h_x, h_y))
        self.hazard.append(Hazard("FugaEspacial/Images/nave.png", h_x, h_y))
        self.hazard.append(Hazard("FugaEspacial/Images/cometaVermelho.png", h_x, h_y))
        self.hazard.append(Hazard("FugaEspacial/Images/meteoros.png", h_x, h_y))
        self.hazard.append(Hazard("FugaEspacial/Images/buracoNegro.png", h_x, h_y))

        #Inicialzia o relógio e o dt que vai limitar o valor de FPS do jogo
        clock = pygame.time.Clock() #inicia o relogio e o dt
        dt = 16 # taxa máxima de frames por segundo. delta time milisec
    
        # Início do loob principal do programa
        while self.run:
            clock.tick(1000 / dt) # controla a velocidade de atulização pelot empo decorrido

            # Handle Input Events
            self.handle_events() #trata eventos

            # Atualiza elementos
            self.elements_update(dt)

            # Desenha o background buffer
            self.elements_draw() #desenha elementos

            # adiciona movimento ao background
            self.background.move(self.screen, self.height, movL_x, movL_y, movR_x, movR_y)
            movL_y = movL_y + velocidade_background
            movR_y = movR_y + velocidade_background

            # se a imagem ultrapassar a extremidade da tela, move de volta
            if movL_y > 600 and movL_y > 600:
                movL_y -= 600
                movR_y -= 600

            # Movimentação do Player
            # Altera a coordenada x da nave de acordo com as mudanças no event_handle() para mover
            x = x + self.mudar_x

            # Desenhar o Player
            self.player.draw(self.screen, x, y) # desenha o player pelo método draw

            # Restrição do movimento do Player
            # Se o player bate na lateral não é Game Over
            if x > 760 - 92 or x < 40 + 5:
                self.screen.blit(self.render_text_bateulateral, (80,200))
                pygame.display.update()  # atualizar a tela
                time.sleep(3)
                self.loop()
                self.run = False

            # adicionando movimento ao hazard
            h_y = h_y + velocidade_hazard / 4 # move pra baixo
            self.hazard[hzrd].draw(self.screen, h_x, h_y) # chama o étodo draw pra desenhar na tela
            h_y = h_y + velocidade_hazard # mantém a velocidade constante a cada quadro

            # definindo onde o hazard vai aparecer, recomeçando a posição d obstaculo e da faixa
            if h_y > self.height: # se passou da tela
                h_y = 0 - h_height # aparece na posição onde hazarde aparece por inteiro
                h_x = random.randrange(125, 650 - h_height) #gerador de movimento
                hzrd = random.randint(0, 4) #hazard aleatorio

            # Atualiza a tela
            pygame.display.update() #atuliza a tela com os elementos masi recentes
            clock.tick(2000) #atualiza a tela. Taxa máxima de atualização. 2000 quadrados por segundo
    # loop()
# Game

# Inicia o jogo: Cria o objeto game e sechama o loob básico
game = Game("resolution", "fullscreen") # instanciar o objeto jogo
game.loop() # iniciar o jogo