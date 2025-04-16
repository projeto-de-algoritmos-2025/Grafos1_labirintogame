import pygame
from collections import deque

# ========== Inicialização ==========
pygame.init()
WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirinto Misterioso")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# ========== Grafo e Dados ==========
grafo = {
    "N1": ["N2", "N3"],
    "N2": ["N1", "N4", "N5"],
    "N3": ["N1", "N6"],
    "N4": ["N2", "N7"],
    "N5": ["N2", "N8"],
    "N6": ["N3", "N9"],
    "N7": ["N4", "N14"],
    "N8": ["N5", "N10"],
    "N9": ["N6", "N11"],
    "N10": ["N8", "N12"],
    "N11": ["N9", "N12"],
    "N12": ["N10", "N11", "N13"],
    "N13": ["N12", "N15"],
    "N14": ["N7"],
    "N15": ["N13"],
}

posicoes = {
    "N1": (100, 350),
    "N2": (250, 250),
    "N3": (180, 550),
    "N4": (400, 200),
    "N5": (320, 350),
    "N6": (300, 500),
    "N7": (580, 180),
    "N8": (460, 360),
    "N9": (460, 520),
    "N10": (600, 300),
    "N11": (580, 520),
    "N12": (700, 400),
    "N13": (800, 400),
    "N14": (700, 120),
    "N15": (900, 400),
}

mensagens_salas = {
    "N2": "Você ouviu um estalo...",
    "N3": "A luz pisca por um momento.",
    "N4": "Uma brisa fria passa por você.",
    "N5": "Um cheiro forte no ar.",
    "N6": "Você vê marcas no chão.",
    "N7": "Silêncio absoluto.",
    "N8": "Algo parece ter se movido.",
    "N9": "Você sente que está sendo observado.",
    "N10": "Passos apressados ecoam...",
    "N11": "Sussurros distantes.",
    "N12": "Será que você está no caminho certo?",
    "N13": "Você chegou quase lá!",
    "N14": "Uma escada para cima, mas está quebrada.",
    "N15": "Ufa, você encontrou a saída!",
}

sala_especial = {
    "N4": -4,
    "N5": +1,
    "N6": -3,
    "N8": +1,
    "N10": -2,
    "N11": -1,
    "N12": +1,
    "N14": -2,
}

inicio = "N1"
final = "N15"
energia = 12
atual = inicio
visitadas = [atual]
jogo_ativo = True
mensagem = "Você desperta em um lugar desconhecido..."
caminho_encontrado = []


# ========== Funções de Busca ==========
def busca_em_largura(grafo, inicio, destino):
    visitados = set()
    fila = deque()
    caminhos = {inicio: [inicio]}

    fila.append(inicio)
    visitados.add(inicio)

    while fila:
        u = fila.popleft()
        for v in grafo[u]:
            if v not in visitados:
                caminhos[v] = caminhos[u] + [v]  # registra caminho até v
                visitados.add(v)
                fila.append(v)
                if v == destino:
                    return caminhos[v]
    return caminhos.get(destino, [])


def busca_em_profundidade(grafo, inicio, destino):
    visitados = set()
    caminho = []

    def dfs_visit(u, caminho_atual):
        visitados.add(u)
        caminho_atual.append(u)
        if u == destino:
            return True
        for v in grafo[u]:
            if v not in visitados:
                if dfs_visit(v, caminho_atual):
                    return True
        caminho_atual.pop()  # backtrack
        return False

    if dfs_visit(inicio, caminho):
        return caminho
    return []


# ========== Funções de Interface ==========
def desenhar_mapa():
    screen.fill((20, 20, 20))
    for sala, vizinhos in grafo.items():
        for v in vizinhos:
            pygame.draw.line(screen, (100, 100, 100), posicoes[sala], posicoes[v], 2)
    for sala, pos in posicoes.items():
        if sala == atual:
            cor = (0, 255, 0)
        elif sala in caminho_encontrado:
            cor = (255, 165, 0)
        elif sala in visitadas:
            cor = (0, 0, 200)
        else:
            cor = (80, 80, 80)
        pygame.draw.circle(screen, cor, pos, 22)
        label = font.render(sala, True, (255, 255, 255))
        screen.blit(label, (pos[0] - 20, pos[1] - 40))


def desenhar_interface():
    info = font.render(f"Energia: {energia}", True, (255, 255, 255))
    msg = font.render(mensagem, True, (255, 255, 0))
    instru = font.render("Pressione B para BFS | D para DFS", True, (200, 200, 200))
    screen.blit(info, (20, 20))
    screen.blit(msg, (20, 60))
    screen.blit(instru, (20, HEIGHT - 40))


def checar_clique(pos_mouse):
    for sala, pos in posicoes.items():
        dx, dy = pos_mouse[0] - pos[0], pos_mouse[1] - pos[1]
        if dx * dx + dy * dy < 25 * 25:
            return sala
    return None


def reiniciar_jogo():
    global atual, energia, visitadas, jogo_ativo, mensagem, sala_especial, caminho_encontrado
    atual = inicio
    energia = 12
    visitadas = [atual]
    jogo_ativo = True
    mensagem = "Você desperta em um lugar desconhecido..."
    caminho_encontrado = []

    # Redefine salas especiais (caso precise reutilizá-las)
    sala_especial = {
        "N4": -4,
        "N5": +1,
        "N6": -3,
        "N8": +1,
        "N10": -2,
        "N11": -1,
        "N12": +1,
        "N14": -2,
    }


# ========== Loop Principal ==========
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and jogo_ativo:
            alvo = checar_clique(evento.pos)
            if alvo and alvo in grafo[atual]:
                energia -= 1
                atual = alvo
                visitadas.append(atual)
                if atual in sala_especial:
                    energia += sala_especial[atual]
                    del sala_especial[atual]
                if energia <= 0:
                    mensagem = "Não foi dessa vez, você morreu."
                    jogo_ativo = False
                elif atual == final:
                    mensagem = "Ufa, você encontrou a saída!"
                    jogo_ativo = False
                else:
                    mensagem = mensagens_salas.get(atual, "")

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_b:
                caminho_encontrado = busca_em_largura(grafo, atual, final)
                mensagem = "BFS executado!"
            if evento.key == pygame.K_d:
                caminho_encontrado = busca_em_profundidade(grafo, atual, final)
                mensagem = "DFS executado!"
            if not jogo_ativo:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        reiniciar_jogo()

    desenhar_mapa()
    desenhar_interface()

    if not jogo_ativo:
        fim = font.render("Pressione R para reiniciar", True, (255, 255, 255))
        screen.blit(fim, (WIDTH // 2 - 140, HEIGHT - 70))

    pygame.display.flip()
    clock.tick(60)

    pygame.display.flip()
    clock.tick(60)
