import pygame
import random

pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirinto Misterioso")
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

grafo = {
    'N1': ['N2', 'N3'],
    'N2': ['N1', 'N4', 'N5'],
    'N3': ['N1', 'N6'],
    'N4': ['N2', 'N7'],
    'N5': ['N2', 'N8'],
    'N6': ['N3', 'N9'],
    'N7': ['N4'],
    'N8': ['N5', 'N10'],
    'N9': ['N6', 'N11'],
    'N10': ['N8', 'N12'],
    'N11': ['N9', 'N12'],
    'N12': ['N10', 'N11', 'N13'],
    'N13': []
}

mensagens_salas = {
    'N2': "Você ouviu um estalo...",
    'N3': "A luz pisca por um momento.",
    'N4': "Uma brisa fria passa por você.",
    'N5': "Um cheiro forte no ar.",
    'N6': "Você vê marcas no chão.",
    'N7': "Silêncio absoluto.",
    'N8': "Algo parece ter se movido.",
    'N9': "Você sente que está sendo observado.",
    'N10': "Passos apressados ecoam...",
    'N11': "Sussurros distantes.",
    'N12': "Será que você está no caminho certo?",
    'N13': "Ufa parece você que chegou ao destino final."
}

sala_especial = {
    'N4': -4,
    'N5': +1,
    'N6': -3,
    'N8': +1,
    'N10': -2,
    'N11': -1,
    'N12': +1
}

posicoes = {
    'N1': (100, 350), 'N2': (282, 250), 'N3': (180, 600),
    'N4': (489, 200), 'N5': (320, 350), 'N6': (300, 500),
    'N7': (700, 220), 'N8': (460, 360), 'N9': (460, 520),
    'N10': (580, 280), 'N11': (580, 520), 'N12': (700, 400),
    'N13': (500, 400)
}

inicio = 'N1'
final = 'N13'
energia = 10
atual = inicio
visitadas = [atual]
jogo_ativo = True
mensagem = "Você desperta em um lugar desconhecido..."

def desenhar_mapa():
    screen.fill((20, 20, 20))
    for sala, vizinhos in grafo.items():
        for v in vizinhos:
            pygame.draw.line(screen, (80, 80, 80), posicoes[sala], posicoes[v], 2)
    for sala, pos in posicoes.items():
        cor = (0, 200, 0) if sala == atual else (0, 0, 200) if sala in visitadas else (60, 60, 60)
        pygame.draw.circle(screen, cor, pos, 25)
        txt = font.render(sala, True, (255, 255, 255))
        rect = txt.get_rect(center=(pos[0], pos[1]-35))
        screen.blit(txt, rect)

def desenhar_interface():
    e_txt = font.render(f"Energia: {energia}", True, (255, 255, 255))
    m_txt = font.render(mensagem, True, (255, 255, 0))
    screen.blit(e_txt, (20, 20))
    screen.blit(m_txt, (20, 60))

def checar_clique(pos_mouse):
    for sala, pos in posicoes.items():
        dx = pos_mouse[0] - pos[0]
        dy = pos_mouse[1] - pos[1]
        if dx * dx + dy * dy < 25 * 25:
            return sala
    return None

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
    desenhar_mapa()
    desenhar_interface()
    pygame.display.flip()
    clock.tick(60)