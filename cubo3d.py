#!/usr/bin/env python3
import math
import os
import sys
import time

# Configurações da tela
LARGURA = 80
ALTURA = 40
TAMANHO_CUBO = 20
DISTANCIA_CAMERA = 100
K1 = 40
INCREMENTO = 0.6

# Ângulos de rotação
A = 0.0
B = 0.0
C = 0.0


def calcular_x(i, j, k, sinA, cosA, sinB, cosB, sinC, cosC):
    return (
        j * sinA * sinB * cosC
        - k * cosA * sinB * cosC
        + j * cosA * sinC
        + k * sinA * sinC
        + i * cosB * cosC
    )


def calcular_y(i, j, k, sinA, cosA, sinB, cosB, sinC, cosC):
    return (
        j * cosA * cosC
        + k * sinA * cosC
        - j * sinA * sinB * sinC
        + k * cosA * sinB * sinC
        - i * cosB * sinC
    )


def calcular_z(i, j, k, sinA, cosA, sinB, cosB):
    return k * cosA * cosB - j * sinA * cosB + i * sinB


def renderizar_ponto(x, y, z, ch, buffer, zbuffer, sinA, cosA, sinB, cosB, sinC, cosC):
    x_rot = calcular_x(x, y, z, sinA, cosA, sinB, cosB, sinC, cosC)
    y_rot = calcular_y(x, y, z, sinA, cosA, sinB, cosB, sinC, cosC)
    z_rot = calcular_z(x, y, z, sinA, cosA, sinB, cosB) + DISTANCIA_CAMERA

    ooz = 1.0 / z_rot

    xp = int(LARGURA / 2 + K1 * ooz * x_rot * 2)
    yp = int(ALTURA / 2 + K1 * ooz * y_rot)

    if 0 <= xp < LARGURA and 0 <= yp < ALTURA:
        idx = xp + yp * LARGURA
        if ooz > zbuffer[idx]:
            zbuffer[idx] = ooz
            buffer[idx] = ch


# Limpa a tela uma vez e esconde o cursor
sys.stdout.write("\x1b[2J\x1b[?25l")

try:
    while True:
        buffer = [" "] * (LARGURA * ALTURA)
        zbuffer = [0.0] * (LARGURA * ALTURA)

        sinA, cosA = math.sin(A), math.cos(A)
        sinB, cosB = math.sin(B), math.cos(B)
        sinC, cosC = math.sin(C), math.cos(C)

        cube_x = -TAMANHO_CUBO
        while cube_x < TAMANHO_CUBO:
            cube_y = -TAMANHO_CUBO
            while cube_y < TAMANHO_CUBO:
                # 6 faces do cubo com caracteres diferentes para profundidade
                renderizar_ponto(
                    cube_x,
                    cube_y,
                    -TAMANHO_CUBO,
                    "@",
                    buffer,
                    zbuffer,
                    sinA,
                    cosA,
                    sinB,
                    cosB,
                    sinC,
                    cosC,
                )
                renderizar_ponto(
                    TAMANHO_CUBO,
                    cube_y,
                    cube_x,
                    "$",
                    buffer,
                    zbuffer,
                    sinA,
                    cosA,
                    sinB,
                    cosB,
                    sinC,
                    cosC,
                )
                renderizar_ponto(
                    -TAMANHO_CUBO,
                    cube_y,
                    -cube_x,
                    "~",
                    buffer,
                    zbuffer,
                    sinA,
                    cosA,
                    sinB,
                    cosB,
                    sinC,
                    cosC,
                )
                renderizar_ponto(
                    -cube_x,
                    cube_y,
                    TAMANHO_CUBO,
                    "#",
                    buffer,
                    zbuffer,
                    sinA,
                    cosA,
                    sinB,
                    cosB,
                    sinC,
                    cosC,
                )
                renderizar_ponto(
                    cube_x,
                    -TAMANHO_CUBO,
                    -cube_y,
                    ";",
                    buffer,
                    zbuffer,
                    sinA,
                    cosA,
                    sinB,
                    cosB,
                    sinC,
                    cosC,
                )
                renderizar_ponto(
                    cube_x,
                    TAMANHO_CUBO,
                    cube_y,
                    "+",
                    buffer,
                    zbuffer,
                    sinA,
                    cosA,
                    sinB,
                    cosB,
                    sinC,
                    cosC,
                )
                cube_y += INCREMENTO
            cube_x += INCREMENTO

        # Reposiciona o cursor no topo sem piscar a tela
        sys.stdout.write("\x1b[H")
        quadro = []
        for i in range(ALTURA):
            quadro.append("".join(buffer[i * LARGURA : (i + 1) * LARGURA]))
        sys.stdout.write("\n".join(quadro))
        sys.stdout.flush()

        A += 0.05
        B += 0.05
        C += 0.01
        time.sleep(0.016)  # ~60 FPS

except KeyboardInterrupt:
    # Restaura o cursor ao sair com Ctrl+C
    sys.stdout.write("\x1b[?25h\n")
    sys.stdout.flush()
