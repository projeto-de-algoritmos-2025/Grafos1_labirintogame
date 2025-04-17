import pygame
from collections import deque


class LabirintoJogo:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1000, 750
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Labirinto Misterioso")
        self.font = pygame.font.SysFont(None, 28)
        self.clock = pygame.time.Clock()

        self.grafo = {
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

        self.posicoes = {
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

        self.mensagens_salas = {
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

        self.inicio = "N1"
        self.final = "N15"
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.atual = self.inicio
        self.energia = 12
        self.visitadas = [self.atual]
        self.jogo_ativo = True
        self.mensagem = "Você desperta em um lugar desconhecido..."
        self.caminho_encontrado = []
        self.sala_especial = {
            "N4": -4,
            "N5": +1,
            "N6": -3,
            "N8": +1,
            "N10": -2,
            "N11": -1,
            "N12": +1,
            "N14": -2,
        }

    def busca_em_largura(self):
        visitados = set()
        fila = deque()
        caminhos = {self.atual: [self.atual]}
        fila.append(self.atual)
        visitados.add(self.atual)

        while fila:
            u = fila.popleft()
            for v in self.grafo[u]:
                if v not in visitados:
                    caminhos[v] = caminhos[u] + [v]
                    visitados.add(v)
                    fila.append(v)
                    if v == self.final:
                        return caminhos[v]
        return caminhos.get(self.final, [])

    def busca_em_profundidade(self):
        visitados = set()
        caminho = []

        def dfs_visit(u, caminho_atual):
            visitados.add(u)
            caminho_atual.append(u)
            if u == self.final:
                return True
            for v in self.grafo[u]:
                if v not in visitados:
                    if dfs_visit(v, caminho_atual):
                        return True
            caminho_atual.pop()
            return False

        if dfs_visit(self.atual, caminho):
            return caminho
        return []

    def desenhar_mapa(self):
        self.screen.fill((20, 20, 20))
        for sala, vizinhos in self.grafo.items():
            for v in vizinhos:
                pygame.draw.line(
                    self.screen,
                    (100, 100, 100),
                    self.posicoes[sala],
                    self.posicoes[v],
                    2,
                )
        for sala, pos in self.posicoes.items():
            if sala == self.atual:
                cor = (0, 255, 0)
            elif sala in self.caminho_encontrado:
                cor = (255, 165, 0)
            elif sala in self.visitadas:
                cor = (0, 0, 200)
            else:
                cor = (80, 80, 80)
            pygame.draw.circle(self.screen, cor, pos, 22)
            label = self.font.render(sala, True, (255, 255, 255))
            self.screen.blit(label, (pos[0] - 20, pos[1] - 40))

    def desenhar_interface(self):
        info = self.font.render(f"Energia: {self.energia}", True, (255, 255, 255))
        msg = self.font.render(self.mensagem, True, (255, 255, 0))
        instru = self.font.render(
            "Pressione B para BFS | D para DFS", True, (200, 200, 200)
        )
        self.screen.blit(info, (20, 20))
        self.screen.blit(msg, (20, 60))
        self.screen.blit(instru, (20, self.HEIGHT - 40))

        if not self.jogo_ativo:
            fim = self.font.render("Pressione R para reiniciar", True, (255, 255, 255))
            self.screen.blit(fim, (self.WIDTH // 2 - 140, self.HEIGHT - 60))

    def checar_clique(self, pos_mouse):
        for sala, pos in self.posicoes.items():
            dx, dy = pos_mouse[0] - pos[0], pos_mouse[1] - pos[1]
            if dx * dx + dy * dy < 25 * 25:
                return sala
        return None

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if evento.type == pygame.MOUSEBUTTONDOWN and self.jogo_ativo:
                    alvo = self.checar_clique(evento.pos)
                    if alvo and alvo in self.grafo[self.atual]:
                        self.energia -= 1
                        self.atual = alvo
                        self.visitadas.append(self.atual)
                        if self.atual in self.sala_especial:
                            self.energia += self.sala_especial[self.atual]
                            del self.sala_especial[self.atual]
                        if self.energia <= 0:
                            self.mensagem = "Não foi dessa vez, você morreu."
                            self.jogo_ativo = False
                        elif self.atual == self.final:
                            self.mensagem = "Ufa, você encontrou a saída!"
                            self.jogo_ativo = False
                        else:
                            self.mensagem = self.mensagens_salas.get(self.atual, "")

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_b:
                        self.caminho_encontrado = self.busca_em_largura()
                        self.mensagem = "BFS executado!"
                    elif evento.key == pygame.K_d:
                        self.caminho_encontrado = self.busca_em_profundidade()
                        self.mensagem = "DFS executado!"
                    elif not self.jogo_ativo and evento.key == pygame.K_r:
                        self.reiniciar_jogo()

            self.desenhar_mapa()
            self.desenhar_interface()
            pygame.display.flip()
            self.clock.tick(60)
