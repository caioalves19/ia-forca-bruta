import pygame
import math
import sys

'''
W, A, S, D: Mover o polígono
Setas (↑, ↓): Modificar o número de lados
+ e -: Modificar o raio
Q e E: Rotacionar o polígono
Z e X: Cisalhamento X
C e V: Cisalhamento Y
SPACE: Centralizar o polígono
ENTER: volta às configurações iniciais do polígono
'''

pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Polígono Interativo")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 100, 255)

pygame.font.init()
fonte = pygame.font.SysFont('Arial', 20)

botao_reset = pygame.Rect(LARGURA - 130, 20, 110, 40)


# Variáveis iniciais
n_lados = 5  
raio = 110
centro_x = LARGURA // 2
centro_y = ALTURA // 2
velocidade = 5  # Velocidade de translação
angulo_rotacao = 0  # Ângulo de rotação
fator_cisalhamento_x = 0  # Fator de cisalhamento no eixo X
fator_cisalhamento_y = 0  # Fator de cisalhamento no eixo Y

# Função para gerar os pontos do polígono com cisalhamento
def gerar_pontos_poligono(n, raio, centro, angulo_rotacao, cisalhamento_x, cisalhamento_y):
    pontos = []
    for i in range(n):
        # Calcula o ângulo de cada ponto
        angulo = (2 * math.pi / n) * i + angulo_rotacao  # Inclui o ângulo de rotação
        x = centro[0] + raio * math.cos(angulo)
        y = centro[1] + raio * math.sin(angulo)

        # Aplica o cisalhamento no eixo X
        x += cisalhamento_x * y

        # Aplica o cisalhamento no eixo Y
        y += cisalhamento_y * x

        pontos.append((x, y))
    return pontos

# Loop principal
clock = pygame.time.Clock()
executando = True
while executando:
    TELA.fill(BRANCO)

    # Verifica os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Verifica teclas pressionadas continuamente
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:  # Move para cima
        centro_y -= velocidade
    if teclas[pygame.K_s]:  # Move para baixo
        centro_y += velocidade
    if teclas[pygame.K_a]:  # Move para a esquerda
        centro_x -= velocidade
    if teclas[pygame.K_d]:  # Move para a direita
        centro_x += velocidade

    # Alterar o número de lados com as teclas para cima e para baixo
    if teclas[pygame.K_UP]:
        n_lados += 1
    elif teclas[pygame.K_DOWN] and n_lados > 3:
        n_lados -= 1

    # Centralizar o polígono ao pressionar a tecla 'Space'
    if teclas[pygame.K_SPACE]:
        centro_x = LARGURA // 2
        centro_y = ALTURA // 2

    # Rotacionar o polígono ao pressionar as teclas 'Q' (esquerda) e 'E' (direita)
    if teclas[pygame.K_q]:
        angulo_rotacao -= 0.05  # Rotaciona para a esquerda
    if teclas[pygame.K_e]:
        angulo_rotacao += 0.05  # Rotaciona para a direita

    # Zera o ângulo ao atingir uma volta completa
    if angulo_rotacao >= 2 * math.pi or angulo_rotacao <= -2 * math.pi:
        angulo_rotacao = 0

    # Escalar o polígono com as teclas '+' e '-' no teclado numérico
    if teclas[pygame.K_KP_PLUS]:  # Tecla '+' do teclado numérico
        raio += 5  # Aumenta o raio
    if teclas[pygame.K_KP_MINUS]:  # Tecla '-' do teclado numérico
        raio -= 5  # Diminui o raio
        if raio < 10:  # Impede que o raio fique muito pequeno
            raio = 10

    # Alterar o fator de cisalhamento com as teclas 'Z' e 'X' (e 'C' e 'V' para Y)
    if teclas[pygame.K_z]:  # Diminuir cisalhamento X
        fator_cisalhamento_x -= 0.05
    if teclas[pygame.K_x]:  # Aumentar cisalhamento X
        fator_cisalhamento_x += 0.05
    if teclas[pygame.K_c]:  # Aumentar cisalhamento Y
        fator_cisalhamento_y += 0.05
    if teclas[pygame.K_v]:  # Diminuir cisalhamento Y
        fator_cisalhamento_y -= 0.05

    #voltar aos valores iniciais
    if teclas[pygame.K_RETURN]:
        n_lados = 5
        raio = 110
        centro_x = LARGURA // 2
        centro_y = ALTURA // 2
        angulo_rotacao = 0
        fator_cisalhamento_x = 0
        fator_cisalhamento_y = 0

    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if botao_reset.collidepoint(evento.pos):
                # Resetar variáveis
                n_lados = 5
                raio = 110
                centro_x = LARGURA // 2
                centro_y = ALTURA // 2
                angulo_rotacao = 0
                fator_cisalhamento_x = 0
                fator_cisalhamento_y = 0

    # Desenha o polígono com cisalhamento
    pontos = gerar_pontos_poligono(n_lados, raio, (centro_x, centro_y), angulo_rotacao, fator_cisalhamento_x, fator_cisalhamento_y)
    pygame.draw.polygon(TELA, AZUL, pontos, 2)

    # Desenha o texto com o número de lados
    texto = fonte.render(f'Lados: {n_lados}', True, (0, 0, 0))
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 10))

    # Desenha o texto com o raio
    texto_raio = fonte.render(f'Raio: {raio}', True, (0, 0, 0))
    TELA.blit(texto_raio, (LARGURA // 2 - texto_raio.get_width() // 2, 40))

    # Exibe o ângulo de rotação
    texto_angulo = fonte.render(f'Ângulo: {math.degrees(angulo_rotacao):.2f}°', True, (0, 0, 0))
    TELA.blit(texto_angulo, (LARGURA // 2 - texto_angulo.get_width() // 2, 70))

    # Exibe o fator de cisalhamento X
    texto_cisalhamento_x = fonte.render(f'Cisalhamento X: {fator_cisalhamento_x:.2f}', True, (0, 0, 0))
    TELA.blit(texto_cisalhamento_x, (LARGURA // 2 - texto_cisalhamento_x.get_width() // 2, 100))

    # Exibe o fator de cisalhamento Y
    texto_cisalhamento_y = fonte.render(f'Cisalhamento Y: {fator_cisalhamento_y:.2f}', True, (0, 0, 0))
    TELA.blit(texto_cisalhamento_y, (LARGURA // 2 - texto_cisalhamento_y.get_width() // 2, 130))

     # Desenha o botão "Resetar"
    pygame.draw.rect(TELA, (200, 200, 200), botao_reset)
    texto_botao = fonte.render("Resetar", True, (0, 0, 0))
    TELA.blit(texto_botao, (botao_reset.centerx - texto_botao.get_width() // 2,
                            botao_reset.centery - texto_botao.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)  # Limita a 30 FPS para controle da movimentação

pygame.quit()
sys.exit()
