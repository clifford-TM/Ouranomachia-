import pygame
import matrizes

pygame.init()

# CORES
Branco = (255, 255, 255)
Preto = (0, 0, 0)
Cinza = (128,128,128)
Azul = (0, 0, 255)


# TELA
largura = 1052
altura = 800
tela = pygame.display.set_mode((largura, altura))

# ELEMENTOS DO TABULEIRO
colunas = 24
quadrados_por_coluna = 31
largura_quadrado = 23
espaco_horizontal = 4
espaco_vertical = 2
x_inicial = 200
y_inicial = 5

# IMAGENS
signos = [pygame.image.load(f"sprites/signos/{i}.png") for i in range(1, 13)]

# Mapeamento dos aspectos às imagens correspondentes
aspectos_info = {
    "ABISMO": {"imagem": pygame.image.load("sprites/casas/abismo.png"), "imagem_negativa": pygame.image.load("sprites/casas/abismo_m.png")},
    "AMAGO": {"imagem": pygame.image.load("sprites/casas/amago.png"), "imagem_negativa": pygame.image.load("sprites/casas/amago_m.png")},
    "CAOS": {"imagem": pygame.image.load("sprites/casas/caos.png"), "imagem_negativa": pygame.image.load("sprites/casas/caos_m.png")},
    "CLARO": {"imagem": pygame.image.load("sprites/casas/claro.png"), "imagem_negativa": pygame.image.load("sprites/casas/claro_m.png")},
    "CONDENAÇÃO": {"imagem": pygame.image.load("sprites/casas/condenação.png"), "imagem_negativa": pygame.image.load("sprites/casas/condenação_m.png")},
    "CONSAGRAÇÃO": {"imagem": pygame.image.load("sprites/casas/consagração.png"), "imagem_negativa": pygame.image.load("sprites/casas/consagração_m.png")},
    "FORTUNA": {"imagem": pygame.image.load("sprites/casas/fortuna.png"), "imagem_negativa": pygame.image.load("sprites/casas/fortuna_m.png")},
    "FUMOSO": {"imagem": pygame.image.load("sprites/casas/fumoso.png"), "imagem_negativa": pygame.image.load("sprites/casas/fumoso_m.png")},
    "JULGAMENTO": {"imagem": pygame.image.load("sprites/casas/julgamento.png"), "imagem_negativa": pygame.image.load("sprites/casas/julgamento_m.png")},
    "MASMORRA": {"imagem": pygame.image.load("sprites/casas/masmorra.png"), "imagem_negativa": pygame.image.load("sprites/casas/masmorra_m.png")},
    "MUTILAÇÃO": {"imagem": pygame.image.load("sprites/casas/mutilacao.png"), "imagem_negativa": pygame.image.load("sprites/casas/mutilacao_m.png")},
    "RENDIÇÃO": {"imagem": pygame.image.load("sprites/casas/rendição.png"), "imagem_negativa": pygame.image.load("sprites/casas/rendição_m.png")},
    "TENEBROSO": {"imagem": pygame.image.load("sprites/casas/tenebroso.png"), "imagem_negativa": pygame.image.load("sprites/casas/tenebroso_m.png")},
    "NULL": {"imagem": pygame.image.load("sprites/casas/null.png"), "imagem_negativa": pygame.image.load("sprites/casas/null_m.png")}
}

casas_signos = [[None for _ in range(colunas)] for _ in range(quadrados_por_coluna)]

# Função para preencher os signos
def preencher_signos(casas_signos, signos):
    for i in range(12):
        casas_signos[0][i] = signos[i]
        casas_signos[0][i + 12] = signos[11 - i]

    
def preencher_casas_aspectos(casas_signos):
    num_linhas = len(matrizes.matriz_completa)

    for i in range(1, num_linhas + 1):
        num_colunas = len(matrizes.matriz_completa[i - 1])
        
        for j in range(num_colunas):
            aspecto, genero = matrizes.matriz_completa[i - 1][j]

            info = aspectos_info.get(aspecto)
            if info:
                if genero == "MASCULINO":
                    casas_signos[i][j] = info["imagem_negativa"]
                    casas_signos[-i][-(j + 1)] = info["imagem_negativa"]  # Inversão 
                else:
                    casas_signos[i][j] = info["imagem"]
                    casas_signos[-i][-(j + 1)] = info["imagem"]  # Inversão 
                


def desenhar_icones(casa, i, j):
            x_out = x_inicial + (largura_quadrado + espaco_horizontal) * i
            y_out = y_inicial + (largura_quadrado + espaco_vertical) * j
            # Desenha os ícones dos signos nas casas
            if casa is not None:
                largura_imagem, altura_imagem = casa.get_size()
                x_desenho = x_out + (largura_quadrado - largura_imagem) // 2
                y_desenho = y_out + (largura_quadrado - altura_imagem) // 2
                tela.blit(casa, (x_desenho, y_desenho))
                
                 

# CONTRUÇÃO DO JOGO
casas = [[0 for _ in range(colunas)] for _ in range(quadrados_por_coluna)]

def tabuleiro():
    numeros_casas = list(range(1, 31))  # Corrigido para começar em 1 e terminar em 30

    for i in range(colunas):
        for j in range(quadrados_por_coluna):
            x_out = x_inicial + (largura_quadrado + espaco_horizontal) * i
            y_out = y_inicial + (largura_quadrado + espaco_vertical) * j

            # Preenche a matriz "casas" com as coordenadas dos quadrados
            casas[j][i] = [x_out, y_out]
            pygame.draw.rect(tela, Cinza, (x_out, y_out, largura_quadrado, largura_quadrado), 3)
            pygame.draw.line(tela, Azul, ((largura/2) - 5, y_inicial), ((largura/2) - 5, altura - 23), 4)
            preencher_casas_aspectos(casas_signos)
            preencher_signos(casas_signos, signos)
            desenhar_icones(casas_signos[j][i], i, j)
            

            # Verifica se está na coluna desejada para exibir o contador
            if i == 1 and j > 0 and j < 31:  # Começa da segunda casa vertical (de cima para baixo)
                casas_1 = numeros_casas[j - 1]
                casas_2 = numeros_casas[30 - j]  # Contagem reversa para a segunda coluna

                # Blit do número da casa na posição desejada
                fonte = pygame.font.Font(None, 20)
                cor_contador = Branco  # Cor do contador
                contador_1 = fonte.render(str(casas_1), True, cor_contador)
                contador_2 = fonte.render(str(casas_2), True, cor_contador)

                # CONTADORES - APENAS PARA REFERÊNCIA 
                tela.blit(contador_1, (x_inicial - 20 , y_out + 5))
                tela.blit(contador_2, ((30 + largura_quadrado * 27) + x_inicial, y_out + 5))

    

    