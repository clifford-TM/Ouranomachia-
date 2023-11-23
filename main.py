import pygame
import main_menu


def jogo():
    import matrizes
    import tabuleiro 
    import pecas

    pygame.init()

    # TELA
    largura = 1052
    altura = 800
    tela = pygame.display.set_mode((largura, altura))

    # NOME E ICONE
    pygame.display.set_caption("Ouranomachia")  
    pygame.display.set_icon(pygame.image.load("sprites/icon.png"))


    # VARIAVEIS IMPORTANTES
    jogador_atual = 1 # JOGADOR QUE COMEÇA
    rodada = -15 # RODADA DO GAME
    fundo = pygame.transform.scale(pygame.image.load("sprites/back.jpg"), (largura, altura))


    clique = False
    novo_clique = False
    rodando = True

    while rodando:

        if jogador_atual == 1:
            jogador = pecas.pecas_jogador1 
        else:
            jogador = pecas.pecas_jogador2

        tela.blit(fundo, (0,0,largura,altura))
        tabuleiro.tabuleiro()

        for peca in pecas.pecas_jogador1 + pecas.pecas_jogador2:
            peca.draw(tela)    
        peca.draw_pontos(tela, largura, pecas.pecas_jogador1, pecas.pecas_jogador2)
                    
        # SAIR DO JOGO
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coordenadas_clique = pygame.mouse.get_pos()
                    limites_matriz = (tabuleiro.x_inicial, tabuleiro.x_inicial + tabuleiro.colunas * (tabuleiro.largura_quadrado + tabuleiro.espaco_horizontal),
                                    tabuleiro.y_inicial + tabuleiro.largura_quadrado, tabuleiro.y_inicial + tabuleiro.quadrados_por_coluna * (tabuleiro.largura_quadrado + tabuleiro.espaco_vertical))

                    # Verifica se as coordenadas do clique estão dentro dos limites
                    if limites_matriz[0] <= coordenadas_clique[0] <= limites_matriz[1] and \
                        limites_matriz[2] <= coordenadas_clique[1] <= limites_matriz[3]:
                        if clique == False:
                            clique = True
                        else:
                            clique = False
                        
                if event.button == 1 and clique == False:
                    novo_clique = True
                    novas_coordenadas = pygame.mouse.get_pos()
                        

        peca_movida = None  # Inicialize como None
        # Se for o turno do jogador 1
        if clique:
            for peca in jogador:
                peca_movida = peca.identificar(coordenadas_clique)
                if peca_movida is not None:
                    peca_movida.mostrar_movimentos()
                    
                if novo_clique:
                    peca_movida.mover(novas_coordenadas)
                    posicao_peca = (peca_movida.linha, peca_movida.coluna)

                    if 0 <= posicao_peca[0] < len(matrizes.matriz_completa) and 0 <= posicao_peca[1] < len(matrizes.matriz_completa[0]):    
                        
                        # REGRA DE COMBATE PARA JOGADOR 2 FORA DO SEU CAMPO 
                        if peca_movida.jogador == 2:
                            peca_movida.perder_pontuacao(1)

                    elif peca_movida.coluna > 12:
                        posicao_peca = (31 - peca_movida.linha, 25 - peca_movida.coluna)

                        # REGRA DE COMBATE PARA JOGADOR 1 FORA DO SEU CAMPO 
                        if peca_movida.jogador == 1:
                            peca_movida.perder_pontuacao(1)

                    aspecto, genero = matrizes.matriz_completa[posicao_peca[0] - 1][posicao_peca[1] - 1]
                    pecas.Peca.calcular_pontuacao(aspecto, genero, peca_movida, posicao_peca)

                    # METODO DE EXPROPIAÇÃO DE PONTOS DO ADVERSÁRIO
                    for peca in pecas.pecas_jogador1 + pecas.pecas_jogador2:
                        if peca_movida != peca and (peca_movida.linha == peca.linha or peca_movida.coluna == peca.coluna):
                            if peca_movida.pontos > peca.pontos and peca_movida.jogador != peca.jogador:
                                peca_movida.expropriar(peca)
                                
                                # METODO DE CAPTURA DE PEÇAS ADVERSÁRIAS 
                                if peca.pontos == 0 and rodada >= 1:
                                    peca.excluir_peca(pecas.pecas_jogador1, pecas.pecas_jogador2)

                        # METODO DE EXPROPIAÇÃO DE PONTOS DO ADVERSÁRIO 
                            elif peca_movida.pontos < peca.pontos and peca_movida.jogador != peca.jogador:
                                peca.expropriar(peca_movida)

                                # METODO DE CAPTURA DE PEÇAS ADVERSÁRIAS 
                                if peca.pontos == 0 and rodada >= 1:
                                    peca.excluir_peca(pecas.pecas_jogador1, pecas.pecas_jogador2)

                    peca_movida = None
                    novo_clique = False
                    clique = False
                    rodada += 1
                    jogador_atual = 3 - jogador_atual 
                    print(rodada) 
                    
        # Atualizar a tela
        pygame.display.flip()

    pygame.quit()

if main_menu.menu():
    jogo()




            
