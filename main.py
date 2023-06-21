"""
Jogo: Fuga Espacial.
Descrição: Um grupo de diplomatas escapam de uma fortaleza estalar a bordo de uma nave danificada.
A nave precisa se desviar das ameaças e sobreviver até atingir a zona de segurança diplomática.
"""

import pygame

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
        self.image = background_fig #atribui a imagem para o background
    
        margin_left_fig = pygame.image.load("FugaEspacial/Images/margin_1.png")
        margin_left_fig.convert()
        margin_left_fig = pygame.transform.scale(margin_left_fig, (60, 602)) #redimensiona a imagem da margem
        self.margin_left = margin_left_fig

        margin_right_fig = pygame.image.load("FugaEspacial/Images/margin_2.png")
        margin_right_fig.convert()
        margin_right_fig = pygame.transform.scale(margin_left_fig, (60, 602)) #redimensiona a imagem da margem
        self.margin_right = margin_right_fig    

    # __init__()

    def update(self, dt):
        pass
    # update()

    def draw(self, screen): 
        screen.blit(self.image, (0,0)) #imagem do background na tela para a cordenada 0,0
        screen.blit(self.margin_left, (0,0)) # 60 depois da primeira margem
        screen.blit(self.margin_right, (740, 0)) # 60 depois da segunda margem
    # draw() 

class Game:
    screen = None #inicializar atributos
    screen_size = None
    width = 800
    height = 600
    run = True
    background = None

    def __init__(self, size, fullscreen):

        """
        Função que inicializa o pygame, define a resolução da tela,
        caption e desabilita o mouse
        """ # Operações
        pygame.init() #inicializar o pygame

        self.screen = pygame.display.set_mode((self.width, self.height)) #tamanho da tela
        self.screen_size = self.screen.get_size() #define o tamnho da tela do jogo

        pygame.mouse.set_visible(0) # desabilita o mouse
        pygame.display.set_caption('Fuga Espacial')

    # init()

    def handle_events(self):
        """
        Trata o evento e toma a ação necessária.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False # interromper o jogo quando clicar em fechar
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

        # Criar o plano de fundo
        self.background = Background() # cria o objeto background

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

            # Atualiza a tela
            pygame.display.update() #atuliza a tela com os elementos masi recentes
            clock.tick(2000) #atualiza a tela. Taxa máxima de atualização. 2000 quadrados por segundo
    # loop()

# Game


# Inicia o jogo: Cria o objeto game e sechama o loob básico
game = Game("resolution", "fullscreen") # instanciar o objeto jogo
game.loop() # iniciar o jogo