import pygame
import os
import random

def menu():
    pygame.init()

    # CORES
    Branco = (255, 255, 255)

    # TELA E PROPORÇÕES
    largura = 1052
    altura = 800
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Ouranomachia")  
    pygame.display.set_icon(pygame.image.load("sprites/icon.png"))

    # IMAGENS
    olho_img = pygame.image.load("sprites/eye_2.png")
    olho = pygame.transform.scale_by(olho_img, 0.85)

    zodiaco_img = pygame.image.load("sprites/zodiac_alt.png")
    zodiaco = pygame.transform.scale_by(zodiaco_img, 0.85)

    fundo = pygame.image.load("sprites/fundo_2.png")

    # Posição e ângulo inicial
    x, y = 130, 0  # Posição inicial
    angle = 0  # Ângulo inicial

    # Carregar a fonte
    fonte = pygame.font.Font(os.path.join(os.getcwd(), "fontes/CELTG.TTF"), 60) 
    fonte_2 = pygame.font.Font(os.path.join(os.getcwd(), "fontes/CELTG.TTF"), 30) 

    # Carregar a música
    musicas = ["musics/main_theme-1.mp3", "musics/main_theme-2.mp3"]
    pygame.mixer.music.load(random.choice(musicas))
    pygame.mixer.music.play(-1)

    # Renderizar o texto
    titulo = fonte.render("OURANOMACHIA", True, Branco)
    textos = [fonte_2.render("Play Game", True, Branco),
            fonte_2.render("Instructions", True, Branco),
            fonte_2.render("Credits", True, Branco)]

    # LOOP PRINCIPAL
    sair = True
    clock = pygame.time.Clock()
    fonte.set_bold(True)
    start = None
    botoes = []

    while sair:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sair = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, botao in enumerate(botoes):
                        if botao.collidepoint(mouse_pos):
                            if i == 0:  # "Play Game" foi clicado
                                start = True

        # Rotaciona a imagem do zodíaco
        zodiaco_rotated = pygame.transform.rotate(zodiaco, angle)
        zodiaco_rect = zodiaco_rotated.get_rect(center=(45 + x + zodiaco.get_width() / 2, 85 + y + zodiaco.get_height() / 2))

        tela.blit(fundo, (0, 0, largura, altura))
        tela.blit(olho, (412, 323, 1, 1))
        tela.blit(zodiaco_rotated, zodiaco_rect)

        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 20))  # Posicione o texto como desejado
        for i, texto in enumerate(textos):
            tela.blit(texto, (415 + largura // 2 - texto.get_width() // 2, 580 + i * 60))
            rect = texto.get_rect()
            rect.topleft = (415 + largura // 2 - texto.get_width() // 2, 580 + i * 60)
            botoes.append(rect)  # Adicionando o retângulo à lista de botões

        # Atualiza o ângulo para a próxima iteração (ajuste a velocidade da rotação conforme necessário)
        angle -= 0.5

        pygame.display.flip()
        pygame.time.delay(10)
        clock.tick(60)  # Limita a taxa de quadros

        if start:
            break

    pygame.quit()
    return start
