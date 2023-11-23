import pygame
import tabuleiro


# CORES
Verde = (0, 255, 0)
Azul = (0, 0, 255)
Branco = (255, 255, 255)
Preto = (0, 0, 0)

# TELA
largura = 1020
altura = 800
tela = pygame.display.set_mode((largura, altura))


class Peca:
     def __init__(self, imagem, linha, coluna, tipo, jogador, pontos):

        # ESCOLHA DO SPRITE DA PEÇA 
        self.imagens = [pygame.image.load(f"sprites/jogadores/{i}.png") for i in range(1, 15)]
        self.imagem = self.imagens[imagem]

        # MAPEAMENTO DO GENERO POR TIPO DA PEÇA
        self.tipo = tipo
        self.genero = {
            "JUPITER": "MASCULINO", 
            "LUA": "FEMININO", 
            "MARTE": "MASCULINO",
            "MERCURIO": "MASCULINO", 
            "SATURNO": "MASCULINO", 
            "SOL": "MASCULINO", 
            "VENUS": "FEMININO"
        }
        self.genero_peca = self.genero.get(self.tipo, None)

        # PONTUAÇÃO
        self.pontos = pontos
        self.jogador = jogador

        # POSICAO
        self.linha = linha
        self.coluna = coluna
        self.rect = self.imagem.get_rect()
        self.atualizar_posicao()

     def atualizar_posicao(self):
        # Calcule as coordenadas x e y com base na linha, coluna e no tamanho dos quadrados do tabuleiro
        x_casa = tabuleiro.x_inicial + ((tabuleiro.largura_quadrado) + tabuleiro.espaco_horizontal) * (self.coluna -1 )
        y_casa = tabuleiro.y_inicial + ((tabuleiro.largura_quadrado) + tabuleiro.espaco_vertical) * (self.linha)

        # Calcule as coordenadas x e y para centralizar a peça na casa
        self.x = x_casa + (tabuleiro.largura_quadrado - self.imagem.get_width()) // 2
        self.y = y_casa + (tabuleiro.largura_quadrado - self.imagem.get_height()) // 2

        self.rect.topleft = (self.x, self.y)


     def draw(self, tela):
        tela.blit(self.imagem, (self.x, self.y))


     def identificar(self, coordenadas):
          if self.rect.collidepoint(coordenadas):
              return self
          else:
              return None


     def mostrar_movimentos(self):
         caminhos = {"JUPITER": {"vertical": 2, "horizontal": 2},
                     "LUA": {"vertical": 11, "horizontal": 11},
                     "MARTE": {"vertical": 3, "horizontal": 3},
                     "MERCURIO": {"vertical": 3, "horizontal": 3},
                     "SATURNO": {"vertical": 2, "horizontal": 2},
                     "SOL": {"vertical": 3, "horizontal": 3},
                     "VENUS": {"vertical": 3, "horizontal": 3}
                    }

         if self.linha + caminhos[self.tipo]["vertical"] > 31: 
             caminhos[self.tipo]["vertical"] = 31 - self.linha

         if self.coluna + caminhos[self.tipo]["horizontal"] > 25:
             caminhos[self.tipo]["horizontal"] = 25 - self.coluna
         
         for i in range(1, caminhos[self.tipo]["vertical"]):
            quadrado_y = self.y + i * (tabuleiro.largura_quadrado + tabuleiro.espaco_vertical)
            pygame.draw.rect(tela, Verde, (self.x + 2, quadrado_y, tabuleiro.largura_quadrado, 24), 2)  

         for i in range(1, caminhos[self.tipo]["horizontal"]):
             quadrado_x = self.x + i * (tabuleiro.largura_quadrado + tabuleiro.espaco_horizontal) + 2
             pygame.draw.rect(tela, Verde, (quadrado_x, self.y, tabuleiro.largura_quadrado,  24), 2)
               


     def mover(self, coordenadas_clique):
          # Calcule a nova posição da peça com base nas coordenadas do clique e na posição inicial da casa
          nova_coluna = (coordenadas_clique[0] - tabuleiro.x_inicial) // (tabuleiro.largura_quadrado + tabuleiro.espaco_horizontal) + 1
          nova_linha = (coordenadas_clique[1] - tabuleiro.y_inicial) // (tabuleiro.largura_quadrado + tabuleiro.espaco_vertical)
          
          # Atualiza a posição da peça para a nova linha e coluna
          if 1 <= nova_coluna <= 24 and 1 <= nova_linha <= 30:
               self.coluna = nova_coluna
               self.linha = nova_linha
               
               # Atualiza a posição da peça de acordo com a nova linha e coluna
               self.pontos = 0
               self.atualizar_posicao()

         
     def pontuacao(self, pontos):
        self.pontos += pontos
        print(f"{self.tipo}, Jogador:{self.jogador}, Pontos: {self.pontos}")


     def perder_pontuacao(self, pontos):
        self.pontos = self.pontos - pontos
        print(f"{self.tipo}, Jogador:{self.jogador}, Pontos: {self.pontos}")


     def calcular_pontuacao(aspecto, genero, peca_movida, posicao_peca):
                    # DIGNIDADES ESSENCIAIS

                    # DOMICILIOS
                    domicilios = {
                         "JUPITER": [9, 12],
                         "LUA": [4],
                         "MARTE":[1, 8],
                         "MERCURIO": [3, 6],
                         "SATURNO": [10, 11],
                         "SOL": [5],
                         "VENUS": [2,7]
                    }

                    if posicao_peca[1] in domicilios[peca_movida.tipo]:
                         peca_movida.pontuacao(5)


                    # EXALTAÇÃO
                    exaltacao = {
                         "JUPITER": 4,
                         "LUA": 2,
                         "MARTE": 10,
                         "MERCURIO": 6,
                         "SATURNO": 7,
                         "SOL": 1,
                         "VENUS": 12
                    }

                    if posicao_peca[1] == exaltacao[peca_movida.tipo]:
                         peca_movida.pontuacao(4)


                    # TRIPLICIDADES
                    triplicidades = {
                         "JUPITER": [1, 5, 9,],
                         "LUA": [2, 6, 10],
                         "MARTE":[4, 8, 12],
                         "MERCURIO": [3, 7, 11],
                         "SATURNO": [3, 7, 11],
                         "SOL": [1, 5, 9,],
                         "VENUS": [2, 6, 10]
                    }
                    
                    if posicao_peca[1] in triplicidades[peca_movida.tipo]:
                         peca_movida.pontuacao(3)

                    
                    # QUEDA
                    queda = {
                         "JUPITER": 10,
                         "LUA": 8,
                         "MARTE": 4,
                         "MERCURIO": 12,
                         "SATURNO": 1,
                         "SOL": 7,
                         "VENUS": 6
                    }
                    if posicao_peca[1] == queda[peca_movida.tipo]:
                         peca_movida.perder_pontuacao(5)
                    

                    # DIGNIDADES SECUNDÁRIAS:

                    # FAVORÁVEIS (GERAIS)
                    favoraveis = {
                         "CLARO": 1, # INDEXAÇÃO DA PONTUAÇÃO NO VALUE DA KEY
                         "FORTUNA": 1,
                         "CONSAGRAÇÃO": 2
                    }
                    if aspecto in favoraveis:
                        peca_movida.pontuacao(favoraveis[aspecto])

                    # DESFAVORÁVEIS (GERAIS)
                    desfavoraveis = {
                         "TENEBROSO": 1, # INDEXAÇÃO DA PONTUAÇÃO NO VALUE DA KEY
                         "MUTILACAO": 1,
                         "MASMORRA": 1,
                         "CAOS": 2,
                         "ABISMO": 2,
                         "RENDIÇÃO": 2,
                         "CONDENAÇÃO": 3
                    }

                    if aspecto in desfavoraveis:
                        peca_movida.perder_pontuacao(desfavoraveis[aspecto])

                    # EXCLUSIVAS

                    # GENERO
                    if genero == peca_movida.genero_peca:
                        peca_movida.pontuacao(1)
                    else:
                        peca_movida.perder_pontuacao(1)

                    # FUMOSO E NAO FUMOSO
                    fumosos = {
                        "FUMOSO": 1,
                        "AMAGO": 2
                    }

                    if aspecto in fumosos and peca_movida.tipo in ["SOL", "LUA"]:
                        peca_movida.pontuacao(fumosos[aspecto])
                    if aspecto in fumosos and peca_movida.tipo not in ["SOL", "LUA"]:
                        peca_movida.perder_pontuacao(fumosos[aspecto])


                    # JUBILOS
                    jubilos = {
                         "JUPITER": 9,
                         "LUA": None,
                         "MARTE": 8,
                         "MERCURIO": 6,
                         "SATURNO": 11,
                         "SOL": None,
                         "VENUS": 2
                    }

                    if posicao_peca[1] == jubilos[peca_movida.tipo]:
                         peca_movida.pontuacao(1)

                    # TERMOS
                    termos = {
                         "JUPITER": [(6,1), (6, 5), (12, 3), (12, 9), (12, 10), (12, 12),
                                     (21, 11), (21, 6), (21, 7), (26,2), (26, 8), (26, 4)],
                         
                         "LUA": [None],
                                     
                         "MARTE": [(9, 4), (9, 8), (25, 3), (25, 1), (25, 11), (28, 6),
                                   (28, 12), (30, 2), (30, 5), (30, 7), (30, 9), (30, 10)],

                         "MERCURIO": [(7,3), (7, 6), (7, 10), (7, 11), (14, 2), (14, 7),
                                     (19, 4), (19, 8), (19, 12), (20, 1), (20, 9), (20, 5)],
                         
                         "SATURNO": [(6, 7), (18, 5), (26, 9), (26, 10), (26, 2), (30, 1),
                                     (30, 3), (30, 4), (30, 6), (30, 8), (30, 11), (30, 12)],

                         "SOL": [None],

                         "VENUS": [(8, 2), (12, 5), (12, 8), (12, 1), (12, 12), (17, 4),
                                     (17, 11), (17, 3), (17, 6), (17, 9), (28, 10), (28, 7)],
                    }
                    
                    if posicao_peca in termos[peca_movida.tipo]:
                        peca_movida.pontuacao(2)

                    
                    # FACES
                    faces = {
                         "JUPITER": [(10, 3), (10, 10), (20, 5), (20, 12), (30, 7)],
                         "LUA": [(10, 7), (20, 2), (20, 9), (30, 4), (30, 10), (30, 11)],
                         "MARTE":[(10, 1), (10, 8), (20, 3), (20, 10), (30, 5), (30, 12)],
                         "MERCURIO": [(10, 2), (10, 9), (20, 4), (20, 11), (30, 6)],
                         "SATURNO": [(10, 5), (10, 12), (20, 7), (30, 2), (30, 9)],
                         "SOL": [(10, 6), (20, 1), (20, 8), (30, 3)],
                         "VENUS": [(10, 5), (10, 12), (20, 7), (30, 2), (30, 9)]
                    }

                    if posicao_peca in faces[peca_movida.tipo]:
                        peca_movida.pontuacao(1)

                    # REGRAS PARA JULGAMENTO
                    if aspecto == "JULGAMENTO":
                         reu = 0
                         if genero != peca_movida.genero_peca:
                             reu += 1

                         if posicao_peca[1] not in domicilios[peca_movida.tipo]:
                             reu += 1 

                         if posicao_peca[1] != exaltacao[peca_movida.tipo]:
                             reu += 1 

                         if posicao_peca[1] not in triplicidades[peca_movida.tipo]:
                             reu += 1

                         if posicao_peca[1] == queda[peca_movida.tipo]:
                             reu += 1

                         if posicao_peca not in termos[peca_movida.tipo]:
                             reu += 1

                         if posicao_peca not in faces[peca_movida.tipo]: 
                             reu += 1
                             

     def draw_pontos(self, tela, largura, pecas_jogador1, pecas_jogador2):
         # Definir a fonte e tamanho do contador de pontos
         fonte = pygame.font.Font(None, 26)
         Preto = (0,0,0)
         Branco = (255,255,255)
         
         # Define as medidas iniciais para aparição dos pontos
         x_pontos_jogador1 = 20
         x_pontos_jogador2 = largura - 60
         
         index_img = {
             "JUPITER":     {1: 1,  2: 2},
             "LUA":         {1: 3,  2: 4},
             "MARTE":       {1: 5,  2: 6},
             "MERCURIO":    {1: 7,  2: 8},
             "SATURNO":     {1: 9,  2: 10},
             "SOL":         {1: 11, 2: 12},
             "VENUS":       {1: 13, 2: 14}
             }
         
         for peca in pecas_jogador1:
            if peca.tipo in index_img:
                if peca.jogador in index_img[peca.tipo]:
                    img_index = index_img[peca.tipo][peca.jogador]
                    y_pos = 50 * img_index
                    tela.blit(self.imagens[img_index - 1], (x_pontos_jogador1, y_pos))
                    texto_pontos_jogador1 = fonte.render(str(peca.pontos), True, Branco)
                    tela.blit(texto_pontos_jogador1, (x_pontos_jogador1 + 30, y_pos + 3))


         for peca in pecas_jogador2:
            if peca.tipo in index_img:
                if peca.jogador in index_img[peca.tipo]:
                    img_index = index_img[peca.tipo][peca.jogador]
                    y_pos = 50 * img_index
                    tela.blit(self.imagens[img_index - 1], (x_pontos_jogador2, y_pos - 50))
                    texto_pontos_jogador2 = fonte.render(str(peca.pontos), True, Branco)
                    tela.blit(texto_pontos_jogador2, (x_pontos_jogador2 + 30, y_pos - 47))
       

     def expropriar(self, inimigo):
          diferenca = self.pontos - inimigo.pontos
          if diferenca > inimigo.pontos:
               self.pontos += inimigo.pontos
               inimigo.pontos = 0
          else:
               self.pontos += diferenca
               inimigo.pontos -= diferenca


     def excluir_peca(self, jogador1, jogador2):
        if self in jogador1:
            jogador1.remove(self)
        elif self in jogador2:
            jogador2.remove(self)

        print(f"{self.tipo} do Jogador {self.jogador} excluído")


     def calcular_jogada_maquina(self, posicao_peca, posicoes_jogador):
         for self in pecas_jogador2:
             posicao_peca = (self.linha, self.coluna)

         for peca in pecas_jogador1:
             posicoes_jogador = (peca.linha, peca.coluna)


             
         

               
                
        
        
        




# FORMATO: IMAGEM, LINHA, COLUNA, TIPO, JOGADOR, PONTOS

# ORDEM: JUPITER, LUA, MARTE, MERCURIO, SATURNO, SOL, VENUS
pecas_jogador1 = [Peca(0, 24, 9, "JUPITER", 1, 0), Peca(2, 18, 4, "LUA", 1, 0), Peca(4, 26, 1, "MARTE", 1, 0),
                  Peca(6, 4, 6, "MERCURIO", 1, 0), Peca(8, 10, 10, "SATURNO", 1, 0), Peca(10, 16, 5, "SOL", 1, 0), Peca(12, 27, 7, "VENUS", 1, 0)]

# ORDEM: VENUS, SOL, SATURNO, MERCURIO, MARTE, LUA, JUPITER
pecas_jogador2 = [Peca(13, 4, 18, "VENUS", 2, 0), Peca(11, 15, 20, "SOL", 2, 0), Peca(9, 21, 15, "SATURNO", 2, 0), Peca(7, 27, 19, "MERCURIO", 2, 0),
                  Peca(5, 5, 24, "MARTE", 2, 0), Peca(3, 13, 21, "LUA", 2, 0), Peca(1, 7, 16, "JUPITER", 2, 0)]


   
