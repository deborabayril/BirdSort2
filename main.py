import pygame
import os
import copy

pygame.init()

# Diretório base
BASE_DIR = r"C:\Users\debor\BirdSort\assets"
if not os.path.exists(BASE_DIR):
    print(f"Erro: O diretório {BASE_DIR} não existe.")
    exit()

LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Bird Sort 2")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)

# Carregar imagem com tratamento de exceções
def carregar_imagem(nome_base):
    for ext in [".png", ".jpg", ".jpeg"]:
        caminho = os.path.join(BASE_DIR, nome_base + ext)
        if os.path.exists(caminho):
            return pygame.image.load(caminho)
    print(f"Erro: Nenhuma versão do arquivo {nome_base} encontrada.")
    exit()

# Carregar imagens
try:
    fundo = carregar_imagem("imagem de fundo")
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

    galho_img = carregar_imagem("galho de arvore")
    galho_img = pygame.transform.scale(galho_img, (250, 80))

    imagens_passaros = {}
    for cor in ["amarelo", "azul", "marrom", "verde", "vermelho"]:
        imagens_passaros[cor] = carregar_imagem(f"passaro {cor}")
        imagens_passaros[cor] = pygame.transform.scale(imagens_passaros[cor], (50, 50))

except Exception as e:
    print(f"Erro ao carregar imagens: {e}")
    exit()

# Estado inicial
estado_jogo = [
    ["vermelho", "marrom", "azul", "verde"],
    ["azul", "verde", "marrom", "vermelho"],
    ["vermelho", "verde", "amarelo"],
    ["azul", "amarelo", "marrom"],
    ["amarelo"],
    []
]

histórico_jogadas = [copy.deepcopy(estado_jogo)]
nivel = 1
estrelas = 3
pausado = False
passaro_selecionado = None
galho_selecionado = None

# Definindo as posições dos galhos globalmente
posicoes = [
    (0, 100), (0, 250), (0, 400),
    (LARGURA - 250, 100), (LARGURA - 250, 250), (LARGURA - 250, 400)
]

# Função para voltar uma jogada
def voltar_uma_jogada():
    global estado_jogo, histórico_jogadas
    if len(histórico_jogadas) > 1:
        histórico_jogadas.pop()
        estado_jogo = copy.deepcopy(histórico_jogadas[-1])

# Função para desenhar troncos e pássaros
def desenhar_troncos():
    tela.blit(fundo, (0, 0))
    
    for i, (galho_x, galho_y) in enumerate(posicoes):
        galho = pygame.transform.flip(galho_img, True, False) if i >= 3 else galho_img
        tela.blit(galho, (galho_x, galho_y))
        for j, cor in enumerate(estado_jogo[i]):
            if cor in imagens_passaros:
                tela.blit(imagens_passaros[cor], (galho_x + 50 * j, galho_y - 40))
    
    pygame.display.update()

# Função para desenhar botões (com ícones mais intuitivos)
def desenhar_botoes():
    pygame.draw.rect(tela, BRANCO, (10, 10, 50, 50), border_radius=10)
    pygame.draw.line(tela, PRETO, (20, 35), (50, 35), 5)
    
    pygame.draw.rect(tela, BRANCO, (LARGURA - 60, 10, 50, 50), border_radius=10)
    pygame.draw.rect(tela, PRETO, (LARGURA - 45, 20, 10, 30))
    pygame.draw.rect(tela, PRETO, (LARGURA - 30, 20, 10, 30))
    
    pygame.draw.rect(tela, BRANCO, (LARGURA // 2 - 100, ALTURA - 60, 80, 50), border_radius=10)
    pygame.draw.polygon(tela, PRETO, [(LARGURA // 2 - 70, ALTURA - 40),
                                       (LARGURA // 2 - 50, ALTURA - 20),
                                       (LARGURA // 2 - 50, ALTURA - 60)]) 


# Função para desenhar layout
def desenhar_layout():
    desenhar_nivel_e_estrelas()
    desenhar_botoes()

# Função para desenhar nível e estrelas
def desenhar_nivel_e_estrelas():
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(f"Nível {nivel}", True, BRANCO)
    tela.blit(texto, (LARGURA // 2 - 50, 30))
    for i in range(estrelas):
        pygame.draw.circle(tela, AMARELO, (200 + i * 30, 100), 10)

# Função para verificar vitória
def verificar_vitoria():
    for galho in estado_jogo:
        if len(galho) > 0 and len(set(galho)) > 1:
            return False
    return True

# Função para calcular estrelas
def calcular_estrelas():
    movimentos = len(histórico_jogadas) - 1
    if movimentos <= 10:
        return 3
    elif movimentos <= 20:
        return 2
    else:
        return 1

# Função para detectar clique no pássaro
def detectar_clique_passaro(x, y):
    global passaro_selecionado, galho_selecionado
    for i, (galho_x, galho_y) in enumerate(posicoes):
        if len(estado_jogo[i]) > 0:
            for j, cor in enumerate(estado_jogo[i]):
                passaro_x = galho_x + 50 * j
                passaro_y = galho_y - 40
                if passaro_x < x < passaro_x + 50 and passaro_y < y < passaro_y + 50:
                    passaro_selecionado = (i, j)
                    galho_selecionado = i
                    return True
    return False

# Função para verificar movimento válido
def movimento_valido(galho_origem, galho_destino):
    if len(estado_jogo[galho_destino]) == 0 or estado_jogo[galho_destino][-1] == estado_jogo[galho_origem][-1]:
        if len(estado_jogo[galho_destino]) < 4:
            return True
    return False

# Função para mover pássaro
def mover_passaro():
    global estado_jogo, passaro_selecionado, galho_selecionado
    if passaro_selecionado and galho_selecionado is not None:
        cor_passaro = estado_jogo[passaro_selecionado[0]][passaro_selecionado[1]]
        for i in range(6):
            if i != galho_selecionado and movimento_valido(galho_selecionado, i):
                estado_jogo[i].append(cor_passaro)
                estado_jogo[galho_selecionado].remove(cor_passaro)
                break
        passaro_selecionado = None

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 10 < x < 60 and 10 < y < 60:
                estado_jogo = copy.deepcopy(histórico_jogadas[0])
            elif LARGURA - 60 < x < LARGURA - 10 and 10 < y < 60:
                pausado = not pausado
            elif LARGURA // 2 - 100 < x < LARGURA // 2 - 20 and ALTURA - 60 < y < ALTURA - 10:
                voltar_uma_jogada()
            elif LARGURA // 2 + 30 < x < LARGURA // 2 + 110 and ALTURA - 60 < y < ALTURA - 10:
                mover_passaro()
            else:
                detectar_clique_passaro(x, y)
    
    desenhar_troncos()
    desenhar_layout()

    if verificar_vitoria():
        estrelas = calcular_estrelas()
        nivel += 1
        estado_jogo = [[""] * 4 for _ in range(6)]
        histórico_jogadas = [copy.deepcopy(estado_jogo)]
    
    pygame.display.update()

pygame.quit()
