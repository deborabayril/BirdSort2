import pygame
from pygame.locals import *
import random
from search import Estado, bfs, custo_uniforme, gulosa, a_star, heuristica

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

LARGURA = 800
ALTURA = 600

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Bird Sort 2")
fonte = pygame.font.Font(None, 36)


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


def rodar_jogo():
    estado = estado_inicial()
    algoritmo = "bfs"
    rodando = True
    movimentos = []

    while rodando:
        desenhar_estado(estado)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                rodando = False
            elif evento.type == KEYDOWN:
                if evento.key == K_r:
                    resultado = resolver_jogo(algoritmo, estado)
                    if resultado:
                        movimentos = []
                        while resultado.movimento:
                            movimentos.append(resultado.jogo)
                            resultado = resultado.movimento  # Volta pelos movimentos
                        movimentos.reverse()
        
        if movimentos:
            estado = movimentos.pop(0)  # Exibe um passo por vez
            pygame.time.delay(500)
        
    pygame.quit()

rodar_jogo()
