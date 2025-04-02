import pygame
from pygame.locals import *
import random
from search import Estado, bfs, custo_uniforme, gulosa, a_star, heuristica
import copy

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

LARGURA = 800
ALTURA = 600

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Bird Sort 2")
fonte = pygame.font.Font(None, 36)

estado_jogo = []
passaro_selecionado = None
galho_selecionado = None
histórico_jogadas = []


def estado_inicial():
    cores = ["amarelo", "azul", "verde", "vermelho", "marrom"]
    estado = [[] for _ in range(6)]  # 5 galhos + 1 vazio
    todos_passaros = cores * 4  # 4 pássaros de cada cor
    random.shuffle(todos_passaros)
    for passaro in todos_passaros:
        for galho in estado:
            if len(galho) < 4:
                galho.append(passaro)
                break
    return estado


def desenhar_estado(estado):
    tela.fill(BRANCO)
    for i, galho in enumerate(estado):
        pygame.draw.rect(tela, PRETO, (100 + i * 120, 200, 80, 200), 2)
        for j, passaro in enumerate(galho):
            cor = VERMELHO if passaro == "vermelho" else PRETO
            pygame.draw.circle(tela, cor, (140 + i * 120, 360 - j * 40), 15)
    botao_resolver = fonte.render("Resolver (R)", True, PRETO)
    tela.blit(botao_resolver, (LARGURA - 200, 20))
    pygame.display.update()


def resolver_jogo(algoritmo, estado_inicial):
    estado_inicial_obj = Estado(estado_inicial, None, 0, heuristica(estado_inicial))
    if algoritmo == "bfs":
        return bfs(estado_inicial_obj)
    elif algoritmo == "custo_uniforme":
        return custo_uniforme(estado_inicial_obj)
    elif algoritmo == "gulosa":
        return gulosa(estado_inicial_obj)
    elif algoritmo == "a_star":
        return a_star(estado_inicial_obj)
    return None


# Função para mover pássaro
def mover_passaro(destino):
    global estado_jogo, passaro_selecionado, galho_selecionado
    if passaro_selecionado and galho_selecionado is not None:
        origem = galho_selecionado
        cor_passaro = estado_jogo[origem][-1]  # Get the top bird from the origin branch
        if movimento_valido(origem, destino):  # Check if the move is valid
            estado_jogo[destino].append(cor_passaro)  # Add the bird to the destination branch
            estado_jogo[origem].pop()  # Remove the bird from the origin branch
            histórico_jogadas.append(copy.deepcopy(estado_jogo))  # Save the move to history
        passaro_selecionado = None  # Reset selection
        galho_selecionado = None


def rodar_jogo():
    global estado_jogo
    estado_jogo = estado_inicial()
    algoritmo = "bfs"
    rodando = True
    movimentos = []

    posicoes = [(100 + i * 120, 200) for i in range(6)]

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Check if the user clicked on a branch
                for i, (galho_x, galho_y) in enumerate(posicoes):
                    if galho_x < x < galho_x + 250 and galho_y - 40 < y < galho_y + 80:
                        if passaro_selecionado is None:  # No bird selected yet
                            if len(estado_jogo[i]) > 0:  # Branch is not empty
                                passaro_selecionado = (i, len(estado_jogo[i]) - 1)
                                galho_selecionado = i
                                print(f"Selecionado pássaro do galho {i}")
                        else:  # A bird is already selected
                            mover_passaro(i)  # Try to move the bird to the clicked branch
                        break
                else:
                    # Reset selection if clicked outside branches
                    passaro_selecionado = None
                    galho_selecionado = None

        desenhar_estado(estado_jogo)

        if movimentos:
            estado_jogo = movimentos.pop(0)  # Exibe um passo por vez
            pygame.time.delay(500)

    pygame.quit()


rodar_jogo()
