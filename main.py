import pygame
import os
import copy

pygame.init()

# Diretório base
# Update the BASE_DIR to use the absolute path
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
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

# Add this at the start of your script
clock = pygame.time.Clock()

# Global variables
rodando = True  # Initialize the game loop control variable
fullscreen = False  # Track fullscreen state

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

# Ensure the victory flag is initialized
vitoria_alcancada = False

# Definindo as posições dos galhos globalmente
posicoes = [
    (0, 100), (0, 250), (0, 400),
    (LARGURA - 250, 100), (LARGURA - 250, 250), (LARGURA - 250, 400)
]

# Create a surface for static elements
static_surface = pygame.Surface((LARGURA, ALTURA))
static_surface.fill(PRETO)  # Fill with the background color
static_surface.blit(fundo, (0, 0))  # Draw the background image

# Draw static elements (buttons) on the static surface
def desenhar_elementos_estaticos():
    # First button (e.g., Undo)
    pygame.draw.rect(static_surface, BRANCO, (10, 10, 50, 50), border_radius=10)
    pygame.draw.line(static_surface, PRETO, (20, 35), (50, 35), 5)

    # Second button (Pause button)
    pygame.draw.rect(static_surface, BRANCO, (LARGURA - 60, 10, 50, 50), border_radius=10)
    pygame.draw.rect(static_surface, PRETO, (LARGURA - 45, 20, 10, 30))  # Left bar of pause icon
    pygame.draw.rect(static_surface, PRETO, (LARGURA - 30, 20, 10, 30))  # Right bar of pause icon

    # Third button (Fullscreen button)
    pygame.draw.rect(static_surface, BRANCO, (LARGURA - 110, 10, 50, 50), border_radius=10)
    pygame.draw.rect(static_surface, PRETO, (LARGURA - 100, 20, 30, 30), 2)  # Square icon for fullscreen

# Função para voltar uma jogada
def voltar_uma_jogada():
    global estado_jogo, histórico_jogadas
    if len(histórico_jogadas) > 1:
        histórico_jogadas.pop()
        estado_jogo = copy.deepcopy(histórico_jogadas[-1])

# Função para desenhar troncos e pássaros
def desenhar_troncos():
    tela.blit(static_surface, (0, 0))  # Draw the static surface
    
    for i, (galho_x, galho_y) in enumerate(posicoes):
        galho = pygame.transform.flip(galho_img, True, False) if i >= 3 else galho_img
        tela.blit(galho, (galho_x, galho_y))
        for j, cor in enumerate(estado_jogo[i]):
            if cor in imagens_passaros:
                passaro_x = galho_x + 50 * j
                passaro_y = galho_y - 40
                # Highlight the selected bird
                if passaro_selecionado == (i, j):
                    pygame.draw.rect(tela, AMARELO, (passaro_x - 2, passaro_y - 2, 54, 54), 3)  # Highlight border
                tela.blit(imagens_passaros[cor], (passaro_x, passaro_y))
    
    pygame.display.update()

# Função para desenhar botões (com ícones mais intuitivos)
def desenhar_botoes():
    # First button (e.g., Undo)
    pygame.draw.rect(tela, BRANCO, (10, 10, 50, 50), border_radius=10)
    pygame.draw.line(tela, PRETO, (20, 35), (50, 35), 5)

    # Second button (Pause button)
    pygame.draw.rect(tela, BRANCO, (LARGURA - 60, 10, 50, 50), border_radius=10)
    pygame.draw.rect(tela, PRETO, (LARGURA - 45, 20, 10, 30))  # Left bar of pause icon
    pygame.draw.rect(tela, PRETO, (LARGURA - 30, 20, 10, 30))  # Right bar of pause icon

    # Third button (Fullscreen button)
    pygame.draw.rect(tela, BRANCO, (LARGURA - 110, 10, 50, 50), border_radius=10)
    pygame.draw.rect(tela, PRETO, (LARGURA - 100, 20, 30, 30), 2)  # Square icon for fullscreen

# Função para desenhar layout
def desenhar_layout():
    desenhar_nivel_e_estrelas()
    desenhar_botoes()

# Função para desenhar nível (sem estrelas)
def desenhar_nivel_e_estrelas():
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render(f"Nível {nivel}", True, BRANCO)
    tela.blit(texto, (LARGURA // 2 - 50, 30))

# Função para verificar vitória
def verificar_vitoria():
    cores_em_galhos = {}  # Dicionário para rastrear em quais galhos cada cor aparece

    for i, galho in enumerate(estado_jogo):
        if len(galho) > 0:
            if len(set(galho)) > 1:  # Mais de uma cor no mesmo galho
                return False
            cor = galho[0]
            if cor not in cores_em_galhos:
                cores_em_galhos[cor] = set()
            cores_em_galhos[cor].add(i)  # Adiciona o índice do galho onde a cor aparece

    # Verifica se cada cor está presente em apenas um galho
    for galhos in cores_em_galhos.values():
        if len(galhos) > 1:  # A cor aparece em mais de um galho
            return False

    # Verifica se todas as cores possíveis estão agrupadas
    todas_cores = set(imagens_passaros.keys())  # Todas as cores possíveis
    return set(cores_em_galhos.keys()) == todas_cores

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
        if len(estado_jogo[i]) > 0:  # Branch is not empty
            passaro_x = galho_x
            passaro_y = galho_y - 40
            if passaro_x < x < passaro_x + 250 and passaro_y < y < galho_y + 80:
                passaro_selecionado = (i, 0)  # Seleciona o pássaro mais à esquerda (índice 0)
                galho_selecionado = i
                print(f"Selecionado pássaro do galho {i}, posição mais à esquerda")
                return True
    return False

# Função para verificar movimento válido
def movimento_valido(galho_origem, galho_destino):
    global passaro_selecionado
    if passaro_selecionado is None:
        return False  # Nenhum pássaro foi selecionado

    _, indice_passaro = passaro_selecionado  # Obtemos o índice do pássaro selecionado
    cor_passaro = estado_jogo[galho_origem][indice_passaro]  # Cor do pássaro selecionado

    # Verifica se o galho de destino está vazio ou se a cor do último pássaro no destino é igual à cor do pássaro selecionado
    if len(estado_jogo[galho_destino]) == 0 or estado_jogo[galho_destino][-1] == cor_passaro:
        if len(estado_jogo[galho_destino]) < 4:  # Verifica se o galho de destino não está cheio
            return True
    return False

# Função para mover pássaro
def mover_passaro(destino):
    global estado_jogo, passaro_selecionado, galho_selecionado
    if passaro_selecionado and galho_selecionado is not None:
        origem, indice_passaro = passaro_selecionado  # Obtemos o galho e o índice do pássaro selecionado
        cor_passaro = estado_jogo[origem][indice_passaro]  # Pegamos o pássaro selecionado
        if movimento_valido(origem, destino):  # Verifica se o movimento é válido
            estado_jogo[destino].append(cor_passaro)  # Adiciona o pássaro ao galho de destino
            estado_jogo[origem].pop(indice_passaro)  # Remove o pássaro do galho de origem
            histórico_jogadas.append(copy.deepcopy(estado_jogo))  # Salva o estado no histórico
        passaro_selecionado = None  # Reseta a seleção
        galho_selecionado = None

# Função para exibir o menu de pausa
def exibir_menu_pausa():
    global pausado, rodando

    # Dimensões do menu de pausa
    largura_menu = 300
    altura_menu = 200
    x_menu = (LARGURA - largura_menu) // 2
    y_menu = (ALTURA - altura_menu) // 2

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pausado = False
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Botão "Resume"
                if x_menu + 50 < x < x_menu + 250 and y_menu + 50 < y < y_menu + 100:
                    pausado = False
                    return
                # Botão "Quit"
                elif x_menu + 50 < x < x_menu + 250 and y_menu + 120 < y < y_menu + 170:
                    rodando = False
                    pausado = False
                    return

        # Desenhar o menu de pausa
        pygame.draw.rect(tela, BRANCO, (x_menu, y_menu, largura_menu, altura_menu), border_radius=10)
        fonte = pygame.font.Font(None, 36)
        texto_pausa = fonte.render("Jogo Pausado", True, PRETO)
        tela.blit(texto_pausa, (x_menu + 80, y_menu + 20))

        # Botão "Resume"
        pygame.draw.rect(tela, AMARELO, (x_menu + 50, y_menu + 50, 200, 50), border_radius=10)
        texto_resume = fonte.render("Resume", True, PRETO)
        tela.blit(texto_resume, (x_menu + 110, y_menu + 60))

        # Botão "Quit"
        pygame.draw.rect(tela, AMARELO, (x_menu + 50, y_menu + 120, 200, 50), border_radius=10)
        texto_quit = fonte.render("Quit", True, PRETO)
        tela.blit(texto_quit, (x_menu + 130, y_menu + 130))

        pygame.display.update()
        clock.tick(30)  # Limit the frame rate for the pause menu

# Função para exibir a janela de vitória
def exibir_janela_vitoria(estrelas):
    global rodando

    # Dimensões da janela de vitória
    largura_janela = 400
    altura_janela = 300
    x_janela = (LARGURA - largura_janela) // 2
    y_janela = (ALTURA - altura_janela) // 2

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Botão "Quit"
                if x_janela + 100 < x < x_janela + 300 and y_janela + 200 < y < y_janela + 250:
                    rodando = False
                    return

        # Desenhar a janela de vitória
        pygame.draw.rect(tela, BRANCO, (x_janela, y_janela, largura_janela, altura_janela), border_radius=10)
        fonte = pygame.font.Font(None, 48)
        texto_vitoria = fonte.render("Você Venceu!", True, PRETO)
        tela.blit(texto_vitoria, (x_janela + 100, y_janela + 50))

        # Desenhar estrelas
        for i in range(estrelas):
            pygame.draw.circle(tela, AMARELO, (x_janela + 150 + i * 40, y_janela + 120), 15)

        # Botão "Quit"
        pygame.draw.rect(tela, AMARELO, (x_janela + 100, y_janela + 200, 200, 50), border_radius=10)
        texto_quit = fonte.render("Quit", True, PRETO)
        tela.blit(texto_quit, (x_janela + 160, y_janela + 210))

        pygame.display.update()
        clock.tick(30)  # Limit the frame rate for the win window

# Loop principal do jogo
# Draw static elements once
desenhar_elementos_estaticos()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # Verifica se o botão de "voltar" (canto superior esquerdo) foi clicado
            if 10 < x < 60 and 10 < y < 60:
                voltar_uma_jogada()  # Chama a função para voltar uma jogada
                print("Voltou uma jogada")
            # Check if the fullscreen button (top-right square) is clicked
            elif LARGURA - 110 < x < LARGURA - 60 and 10 < y < 60:
                fullscreen = not fullscreen  # Toggle fullscreen state
                if fullscreen:
                    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
                else:
                    tela = pygame.display.set_mode((LARGURA, ALTURA))  # Return to windowed mode
            # Check if the pause button (second button) is clicked
            elif LARGURA - 60 < x < LARGURA - 10 and 10 < y < 60:
                pausado = True
                exibir_menu_pausa()  # Show the pause menu
            # Handle other clicks (e.g., bird movement) only if not paused
            if not pausado:
                for i, (galho_x, galho_y) in enumerate(posicoes):
                    if galho_x < x < galho_x + 250 and galho_y - 40 < y < galho_y + 80:
                        if passaro_selecionado is None:  # Nenhum pássaro selecionado ainda
                            if len(estado_jogo[i]) > 0:  # O galho não está vazio
                                if i >= 3:  # Galhos do lado direito
                                    passaro_selecionado = (i, 0)  # Seleciona o pássaro mais à esquerda
                                else:  # Galhos do lado esquerdo
                                    passaro_selecionado = (i, len(estado_jogo[i]) - 1)  # Seleciona o pássaro mais à direita
                                galho_selecionado = i
                                print(f"Selecionado pássaro do galho {i}")
                        else:  # Um pássaro já está selecionado
                            mover_passaro(i)  # Tenta mover o pássaro para o galho clicado

                            # Atualiza a tela para mostrar o movimento antes de verificar a vitória
                            desenhar_troncos()
                            pygame.display.flip()  # Atualiza a tela com o novo estado do jogo

                            # Verifica vitória após o movimento
                            if verificar_vitoria() and not vitoria_alcancada:
                                estrelas = calcular_estrelas()
                                nivel += 1
                                vitoria_alcancada = True  # Marca a vitória como processada
                                print(f"Vitória! Avançando para o nível {nivel}.")
                                exibir_janela_vitoria(estrelas)  # Mostra a janela de vitória
                                # Reinicia o estado do jogo para o próximo nível
                                estado_jogo = [[""] * 4 for _ in range(6)]
                                histórico_jogadas = [copy.deepcopy(estado_jogo)]
                        break
                else:
                    # Reseta a seleção se clicar fora dos galhos
                    passaro_selecionado = None
                    galho_selecionado = None

    # Skip game updates if paused
    if pausado:
        continue

    # Reset the victory flag when the game state changes
    if not verificar_vitoria():
        vitoria_alcancada = False

    # Draw static elements (background and buttons)
    tela.blit(static_surface, (0, 0))

    # Draw dynamic elements (birds and game state)
    desenhar_troncos()

    pygame.display.flip()  # Update the entire screen
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
